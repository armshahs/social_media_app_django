A social media app where users can add friends, create posts, add comments, send friend requests, receive notifications, follow hashtag trends, report posts, etc.

Certainly! Grouping URL endpoints under headings can make the README more organized and easier to navigate. Here's the updated version with URL endpoints grouped under headings:

---

# Social Media App using Django

![Social Media App](https://via.placeholder.com/800x400)

## Overview

This project is a social media application built using Django, allowing users to create profiles, post updates, follow other users, like and comment on posts, and more. It provides a foundation for building a basic social networking platform.

## Features

- **User Authentication:** Allow users to register, login, and manage their accounts.
- **Profiles:** Users can create and edit their profiles, including uploading a profile picture and providing personal information.
- **Posts:** Users can create, edit, and delete posts.
- **Following/Followers:** Users can follow other users and see updates from users they follow.
- **Likes and Comments:** Users can like and comment on posts.
- **Search:** Basic search functionality to find users or posts.

## Installation

### Prerequisites

- Python 3.x
- Django

### Steps

1. Clone the repository:

```bash
git clone https://github.com/armshahs/social_media_app_django.git
```

2. Navigate to the project directory:

```bash
cd social_media_app_django
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply database migrations:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

6. Visit `http://localhost:8000` in your web browser to access the application.

## URL Endpoints

### Authentication

- **Registration:** `/register/`
- **Login:** `/login/`
- **Logout:** `/logout/`

### Profile

- **View Profile:** `/profile/<username>/`
- **Edit Profile:** `/profile/edit/`

### Posts

- **Create Post:** `/post/create/`
- **Edit Post:** `/post/<post_id>/edit/`
- **Delete Post:** `/post/<post_id>/delete/`

### Following/Followers

- **Follow User:** `/follow/<username>/`
- **Unfollow User:** `/unfollow/<username>/`

### Likes and Comments

- **Like Post:** `/post/<post_id>/like/`
- **Unlike Post:** `/post/<post_id>/unlike/`
- **Comment on Post:** `/post/<post_id>/comment/`

### Search

- **Search:** `/search/`

## Usage

1. Register for a new account or login if you already have one.
2. Create and edit your profile by clicking on your username in the navigation bar.
3. Create new posts from the homepage.
4. Follow other users to see their updates on your homepage.
5. Like and comment on posts by other users.
6. Use the search functionality to find users or posts.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature/my-feature` or `git checkout -b bugfix/fix-issue`.
3. Make your changes and commit them: `git commit -am 'Add new feature'`.
4. Push to your branch: `git push origin feature/my-feature`.
5. Submit a pull request detailing your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

Special thanks to [armshahs](https://github.com/armshahs) for creating this project.

---

This format organizes the URL endpoints into sections based on their functionality, making it easier for users to locate the endpoints they need.
