"""
User Profile Management for Search AI Agent
Handles user-specific data and personalization context
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
import random

class UserProfile:
    """Represents a user profile with personalization data."""
    
    def __init__(self, user_id: str = None):
        self.user_id = user_id or self._generate_user_id()
        self.name = ""
        self.city = ""
        self.interests = []
        self.profession = ""
        self.expertise_level = "beginner"  # beginner, intermediate, expert
        self.preferred_topics = []
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
        self.interaction_count = 0
        
    def _generate_user_id(self) -> str:
        """Generate a unique user ID."""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def update_profile(self, **kwargs):
        """Update profile fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.last_updated = datetime.now()
    
    def increment_interaction(self):
        """Increment interaction counter."""
        self.interaction_count += 1
    
    def get_personalization_context(self) -> str:
        """Generate personalization context for the agent."""
        if not self.name:
            return ""
        
        context_parts = [f"You're helping {self.name}"]
        
        if self.city:
            context_parts.append(f"from {self.city}")
        
        if self.profession:
            context_parts.append(f"who works as a {self.profession}")
        
        if self.interests:
            interests_str = ", ".join(self.interests[:3])  # Limit to 3 interests
            context_parts.append(f"who likes {interests_str}")
        
        if self.expertise_level != "beginner":
            context_parts.append(f"with {self.expertise_level} expertise")
        
        if self.preferred_topics:
            topics_str = ", ".join(self.preferred_topics[:2])
            context_parts.append(f"and prefers topics like {topics_str}")
        
        context = " ".join(context_parts) + ". Personalize examples and explanations accordingly."
        return context
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "city": self.city,
            "interests": self.interests,
            "profession": self.profession,
            "expertise_level": self.expertise_level,
            "preferred_topics": self.preferred_topics,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "interaction_count": self.interaction_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        """Create profile from dictionary."""
        profile = cls(data.get("user_id"))
        profile.name = data.get("name", "")
        profile.city = data.get("city", "")
        profile.interests = data.get("interests", [])
        profile.profession = data.get("profession", "")
        profile.expertise_level = data.get("expertise_level", "beginner")
        profile.preferred_topics = data.get("preferred_topics", [])
        profile.created_at = datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
        profile.last_updated = datetime.fromisoformat(data.get("last_updated", datetime.now().isoformat()))
        profile.interaction_count = data.get("interaction_count", 0)
        return profile


class UserProfileManager:
    """Manages user profiles and persistence."""
    
    def __init__(self, storage_file: str = "user_profiles.json"):
        self.storage_file = storage_file
        self.profiles: Dict[str, UserProfile] = {}
        self.load_profiles()
    
    def load_profiles(self):
        """Load profiles from storage file."""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.profiles = {
                        user_id: UserProfile.from_dict(profile_data)
                        for user_id, profile_data in data.items()
                    }
        except Exception as e:
            print(f"Warning: Could not load user profiles: {e}")
            self.profiles = {}
    
    def save_profiles(self):
        """Save profiles to storage file."""
        try:
            data = {
                user_id: profile.to_dict()
                for user_id, profile in self.profiles.items()
            }
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save user profiles: {e}")
    
    def get_or_create_profile(self, user_id: str = None) -> UserProfile:
        """Get existing profile or create a new one."""
        if user_id and user_id in self.profiles:
            profile = self.profiles[user_id]
            profile.increment_interaction()
            return profile
        
        # Create new profile with mock data
        profile = UserProfile(user_id)
        self._populate_mock_data(profile)
        self.profiles[profile.user_id] = profile
        self.save_profiles()
        return profile
    
    def _populate_mock_data(self, profile: UserProfile):
        """Populate profile with realistic mock data."""
        # Mock names
        names = ["Alex", "Sam", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Quinn"]
        profile.name = random.choice(names)
        
        # Mock cities
        cities = ["San Francisco", "New York", "London", "Tokyo", "Berlin", "Sydney", "Toronto", "Paris"]
        profile.city = random.choice(cities)
        
        # Mock interests
        all_interests = [
            "artificial intelligence", "machine learning", "data science", "web development",
            "mobile apps", "cybersecurity", "blockchain", "cloud computing", "IoT", "robotics",
            "quantum computing", "biotechnology", "renewable energy", "space exploration",
            "music", "photography", "cooking", "travel", "fitness", "reading"
        ]
        profile.interests = random.sample(all_interests, random.randint(2, 4))
        
        # Mock professions
        professions = [
            "software engineer", "data scientist", "product manager", "designer",
            "researcher", "consultant", "entrepreneur", "student", "teacher", "analyst"
        ]
        profile.profession = random.choice(professions)
        
        # Mock expertise level
        profile.expertise_level = random.choice(["beginner", "intermediate", "expert"])
        
        # Mock preferred topics
        tech_topics = [
            "AI and machine learning", "web development", "data analysis",
            "cybersecurity", "cloud computing", "mobile development", "DevOps"
        ]
        profile.preferred_topics = random.sample(tech_topics, random.randint(1, 3))
    
    def update_profile(self, user_id: str, **kwargs) -> bool:
        """Update a specific user profile."""
        if user_id in self.profiles:
            self.profiles[user_id].update_profile(**kwargs)
            self.save_profiles()
            return True
        return False
    
    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get a specific user profile."""
        return self.profiles.get(user_id)
    
    def list_profiles(self) -> list:
        """List all user profiles."""
        return list(self.profiles.values())
    
    def delete_profile(self, user_id: str) -> bool:
        """Delete a user profile."""
        if user_id in self.profiles:
            del self.profiles[user_id]
            self.save_profiles()
            return True
        return False


# Global profile manager instance
profile_manager = UserProfileManager()


def get_user_context(user_id: str = None) -> str:
    """Get personalization context for a user."""
    profile = profile_manager.get_or_create_profile(user_id)
    return profile.get_personalization_context()


def update_user_profile(user_id: str, **kwargs) -> bool:
    """Update user profile data."""
    return profile_manager.update_profile(user_id, **kwargs)


def get_user_profile(user_id: str) -> Optional[UserProfile]:
    """Get user profile by ID."""
    return profile_manager.get_profile(user_id) 