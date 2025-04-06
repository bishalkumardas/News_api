from rest_framework import serializers
from .models import Comment, News
import numpy as np
import pickle
from tensorflow.keras.models import load_model # type: ignore
from sklearn.feature_extraction.text import CountVectorizer
from django.conf import settings
import os

vectorizer_path = os.path.join(settings.BASE_DIR, 'comment_api', 'vectorizer.pkl')
model_path = os.path.join(settings.BASE_DIR, 'comment_api', 'news_sentiment_model.h5')

with open(vectorizer_path, 'rb') as f:
    vectorizer = pickle.load(f)

model = load_model(model_path)

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

        # Combine headline and subheadline
        text = headline + " " + subheadline

        # Convert text to numerical features
        text_vector = vectorizer.transform([text]).toarray()
        # Predict sentiment
        predicted_class = np.argmax(model.predict(text_vector), axis=1)[0]

        # Map numeric prediction to sentiment label
        sentiment_map = {0: "Positive", 1: "Neutral", 2: "Negative"}
        return sentiment_map.get(predicted_class, "Unknown")