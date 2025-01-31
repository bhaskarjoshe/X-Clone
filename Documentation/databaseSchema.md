# Database Schema Relationship Diagram

- **User Table (1) → (N) Tweet Table**  
- **User Table (1) → (N) Follow Table** (follower and followed)  
- **Tweet Table (1) → (N) Comment Table**  
- **Tweet Table (1) → (N) Like Table**  
- **Tweet Table (1) → (N) Media Table**  

---

## 1. User Table (User)

The **User** table stores user-specific details like username, email, password, and authentication details.  

### Fields:
- **id** *(Primary Key, AutoField)* - Unique identifier for each user.  
- **username** *(CharField, Unique)* - Unique username for the user.  
- **email** *(EmailField, Unique)* - User's email address.  
- **password** *(CharField)* - Encrypted password for authentication.  
- **first_name** *(CharField, optional)* - First name of the user.  
- **last_name** *(CharField, optional)* - Last name of the user.  
- **profile_picture** *(ImageField, optional)* - URL for the profile image (could be null).  
- **bio** *(TextField, optional)* - Bio or description about the user.  
- **is_power_user** *(BooleanField)* - Determines if the user is a power user (default `False`).  
- **date_joined** *(DateTimeField)* - Timestamp when the user joined.  
- **last_login** *(DateTimeField, nullable)* - Timestamp of the last login.  

---

## 2. Tweet Table (Tweet)

The **Tweet** table stores tweets posted by users. This includes tweet content, user reference, and timestamps.  

### Fields:
- **id** *(Primary Key, AutoField)* - Unique identifier for each tweet.  
- **content** *(TextField)* - The tweet content (max 280 characters for regular users, more for power users).  
- **author** *(ForeignKey to User)* - The user who posted the tweet.  
- **created_at** *(DateTimeField)* - Timestamp when the tweet was created.  
- **updated_at** *(DateTimeField, nullable)* - Timestamp when the tweet was last edited.  
- **is_pinned** *(BooleanField)* - Flag to indicate if the tweet is pinned (available for power users).  
- **is_deleted** *(BooleanField)* - Flag to indicate if the tweet is deleted (soft delete).  

### Relationships:
- **1:N Relationship** *(1 user → many tweets)*  
- **Foreign Key:** `author` (references User)  

---

## 3. Comment Table (Comment)

The **Comment** table stores comments made on tweets. A comment belongs to a specific tweet and is authored by a user.  

### Fields:
- **id** *(Primary Key, AutoField)* - Unique identifier for each comment.  
- **tweet** *(ForeignKey to Tweet)* - The tweet that the comment belongs to.  
- **author** *(ForeignKey to User)* - The user who posted the comment.  
- **content** *(TextField)* - The comment content.  
- **created_at** *(DateTimeField)* - Timestamp when the comment was created.  
- **is_deleted** *(BooleanField)* - Flag to indicate if the comment is deleted (soft delete).  

### Relationships:
- **1:N Relationship** *(1 tweet → many comments)*  
- **1:N Relationship** *(1 user → many comments)*  
- **Foreign Keys:** `tweet` (references Tweet), `author` (references User)  

---

## 4. Follow Table (Follow)

The **Follow** table handles follow/unfollow functionality, storing relationships between users.  

### Fields:
- **id** *(Primary Key, AutoField)* - Unique identifier for each follow relationship.  
- **follower** *(ForeignKey to User)* - The user who is following another user.  
- **followed** *(ForeignKey to User)* - The user being followed.  
- **created_at** *(DateTimeField)* - Timestamp when the follow relationship was created.  

### Relationships:
- **M:N Relationship** *(1 user can follow many users, and 1 user can be followed by many users)*  
- **Foreign Keys:** `follower` (references User), `followed` (references User)  

---

## 5. Like Table (Like)

The **Like** table tracks likes on tweets. A user can like multiple tweets, and each tweet can receive multiple likes.  

### Fields:
- **id** *(Primary Key, AutoField)* - Unique identifier for each like.  
- **tweet** *(ForeignKey to Tweet)* - The tweet that is liked.  
- **user** *(ForeignKey to User)* - The user who liked the tweet.  
- **created_at** *(DateTimeField)* - Timestamp when the like was made.  

### Relationships:
- **1:N Relationship** *(1 tweet → many likes)*  
- **1:N Relationship** *(1 user → many likes)*  
- **Foreign Keys:** `tweet` (references Tweet), `user` (references User)  

---

## 6. Media Table (Media)

The **Media** table stores media files (images/videos) uploaded by users. Tweets can have multiple media files attached.  

### Fields:
- **id** *(Primary Key, AutoField)* - Unique identifier for each media file.  
- **file** *(FileField)* - Media file uploaded (image/video).  
- **tweet** *(ForeignKey to Tweet)* - The tweet associated with this media.  
- **created_at** *(DateTimeField)* - Timestamp when the media was uploaded.  

### Relationships:
- **1:N Relationship** *(1 tweet → multiple media files)*  
- **Foreign Key:** `tweet` (references Tweet)  
