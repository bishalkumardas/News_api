from rest_framework import serializers
from .models import Comment, News
import numpy as np
import pickle
# from tensorflow.keras.models import load_model # type: ignore
from sklearn.feature_extraction.text import CountVectorizer
from django.conf import settings
import os
# from functools import lru_cache

class CommentSerializer(serializers.Serializer):
    fname = serializers.CharField(max_length=50)
    lname = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=254)
    exp = serializers.IntegerField()
    comment = serializers.CharField(max_length=None)
    id = serializers.IntegerField(read_only=True)
    
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'  # Serialize all fields
    
    def create(self, validated_data):
        """
        Override create method to automatically predict sentiment before saving.
        """
        head = validated_data.get("head", "")
        sub_head = validated_data.get("sub_head", "")
        print(head)

        # Predict sentiment
        predicted_sentiment = self.predict_sentiment(head, sub_head)

        # Save the predicted sentiment
        validated_data["sentiment"] = predicted_sentiment
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Override update method to allow manual sentiment editing.
        If the user provides sentiment, it should be saved as it is.
        """
        # Only update the sentiment if the user explicitly provides it
        if "sentiment" in validated_data:
            instance.sentiment = validated_data["sentiment"]

        # Update other fields
        instance.head = validated_data.get("head", instance.head)
        instance.sub_head = validated_data.get("sub_head", instance.sub_head)
        instance.date = validated_data.get("date", instance.date)
        instance.image_link = validated_data.get("image_link", instance.image_link)
        instance.content = validated_data.get("content", instance.content)

        instance.save()
        return instance
    
    def predict_sentiment(self, headline, subheadline):
        """
            Predicts sentiment based on the given headline and subheadline.
            Parameters:
            - headline (str): The headline text.
            - subheadline (str): The subheadline text.

            Returns:
            - sentiment (str): Predicted sentiment ("Positive", "Neutral", "Negative").
        """        
        
        # Define model and vectorizer paths locally
        vectorizer_path = os.path.join(settings.BASE_DIR, 'comment_api', 'vectorizer.pkl')
        model_path = os.path.join(settings.BASE_DIR, 'comment_api', 'news_sentiment_model.h5')


       # Lazy load and cache the model and vectorizer
        if not hasattr(self, 'vectorizer'):
            with open(vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)

        if not hasattr(self, 'model'):
            from tensorflow.keras.models import load_model  # type: ignore # Import only when needed
            self.model = load_model(model_path)

        text = headline + " " + subheadline
        text_vector = self.vectorizer.transform([text]).toarray()
        predicted_class = np.argmax(self.model.predict(text_vector), axis=1)[0]

        sentiment_map = {0: "Positive", 1: "Neutral", 2: "Negative"}
        return sentiment_map.get(predicted_class, "Unknown")