# API Endpoints

## Table of Contents

- [Users](#users)
- [Groups](#groups)
- [Workouts](#workouts)
- [Activities](#activities)
- [Comments](#comments)
- [Suggestions](#suggestions)
- [Memberships](#memberships)

## Users

### User Model:

| Name | Type | Description |
|:-----|:----:|:------------|
| id | int | unique user id. |
| username | char | unique identifier for every user. |
| first_name | char | Users first name. |
| last_name | char | Users last name. |
| bio | text | Users Bio. |
| year | integer | Users graduation year. |
| group | integer | group identifier. |

---

```python
GET api/v1/users/
```

**Description** : Returns a list of User objects

**Auth required** : YES

**Permissions required** : None

### Parameters

|  Name | Required |            Description            | Default | Example |
|:------|:--------:|:----------------------------------|:-------:|:-------:|
| group | No       | Filter by group id                | None    | `group=1`    |
| year  | No       | Filter by graduation year         | None    | `year=2021`  |

**Example Response:**

```json
[
    {
        "id": 1,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "This is my bio.",
        "year": 2021,
        "group": 1,
    },
    {
        "id": 2,
        "username": "janedoe",
        "first_name": "Jane",
        "last_name": "Doe",
        "bio": "This is my bio.\r\nGo Blue!",
        "year": 2022,
        "group": 2,
    },
]
```

---

```python
GET api/v1/users/{user_id}/
```

**Description** : Returns user object with `user_id`

**Auth required** : YES

**Permissions required** : None

**Parameters:** None

**Example Response:**

```json
{
    "id": 1,
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "This is my bio.",
    "year": 2021,
}
```

---

```python
GET api/v1/users/{user_id}/activities/
```

**Description** : Returns a list of Activity summaries for the specified user.

**Auth required** : YES

**Permissions required** : Signed in

### Parameters

|  Name    | Required |              Description              | Default |    Example    |
|:---------|:--------:|:--------------------------------------|:-------:|:-------------:|
|  type    | No       | Returns activities of specified type. | None    | `type=T`      |
|  page    | No       | Page number.                          | 1       | `page=1`      |
| per_page | No       | Results per page.                     |  10     | `per_page=10` |
| sort     | No       | Sort by date ascending or descending. | desc    | `sort=asc`    |

**Example Response:**

```json
[
    {
        "id": 1,
        "user": 1,
        "workout_id": 2,
        "time": "2020-06-21T19:46:45.315Z",
        "comment": "This is a comment.",
        "workout": {
            "id": 2,
            "title": "4x400m",
            "description": "4 min rest between reps. I don't reccomend wearing spikes for these.",
            "category": "T",
            "owner": 1,
        },
    },
    {
        "id": 2,
        "user": 1,
        "workout_id": 2,
        "time": "2020-06-22T19:46:45.315Z",
        "comment": "This is another comment.",
        "workout": {
            "id": 2,
            "title": "4x400m",
            "description": "4 min rest between reps. I don't reccomend wearing spikes for these.",
            "category": "T",
            "owner": 1,
        },
    },
]
```

---

```python
GET api/v1/users/{user_id}/workouts/
```

**Description** : Returns a list of workouts for specified user.

**Auth required** : YES

**Permissions required** : None

[//]: # (Might change this to following later on)

### Parameters

|  Name    | Required |              Description              | Default |    Example    |
|:---------|:--------:|:--------------------------------------|:-------:|:-------------:|
|  type    | No       | Returns workouts of specified type.   | None    | `type=1`      |
|  page    | No       | Page number.                          | 1       | `page=1`      |
| per_page | No       | Results per page.                     |  10     | `per_page=10` |

**Example Response:**

```json
[
    {
        "id": 1,
        "title": "4x400m",
        "description": "4 min rest between reps. I don't reccomend wearing spikes for these.",
        "category": 1,
        "owner": 1,
    },
    {
        "id": 2,
        "title": "30-30s",
        "description": "200s in 30 sec with 30 sec rest. I usually do 6-8 of them. If you arent in shape these are pretty tough so you can aim for a longer time like all under 35s for example. If you aren't hitting the time either make it higher or take a 5 min rest halfway through.",
        "category": 1,
        "owner": 1,
    },
]
```

---

```python
GET api/v1/users/me/
```

**Description** : Returns logged in user.

**Auth required** : YES

**Permissions required** : None

### Parameters

None

**Example Response:**

```json
{
    "id": 1,
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "This is my bio.",
    "year": 2021,
    "group": 1,
}
```

---

```python
PATCH api/v1/users/me/
```

**Description** : Allows modifying your user object.

**Auth required** : YES

**Permissions required** : None

### Parameters

None

**Example Response:**

```json
{
    "id": 1,
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "This is my bio.",
    "year": 2021,
    "group": 1,
}
```

---

## Groups
### Group Model:

| Name | Type | Description |
|:-----|:----:|:------------|
| id | integer | Unique group identifier. |
| name | char | Group name. |
| description | text | Group description. |

---

```python
GET api/v1/groups/
```

**Description** : Returns a list of group objects

**Auth required** : YES

**Permissions required** : None

**Parameters:** None

**Example Response:**

```json
[
    {
        "id": 1,
        "name": "Short Sprints",
        "description": "100m and 200m specialists.",
    },
    {
        "id": 2,
        "name": "Long Sprints",
        "description": "200m and 400m specialists.",
    },
]
```

---

```python
POST api/v1/groups/
```

**Description** : Create a group

**Auth required** : YES

**Permissions required** : Admin

**Parameters:** None

---

```python
PATCH api/v1/groups/{group_id}/
```

**Description** : Modify a group

**Auth required** : YES

**Permissions required** : Admin

**Parameters:** None

---

```python
DELETE api/v1/groups/{group_id}/
```

**Description** : Removes a group

**Auth required** : YES

**Permissions required** : Admin

**Parameters:** None

---

```python
GET api/v1/groups/{group_id}/members/
```

**Description** : Returns a list of User objects

**Auth required** : YES

**Permissions required** : Admin

[//]: # (Might change this to following later on)

### Parameters

|  Name    | Required |              Description              | Default |    Example    |
|:---------|:--------:|:--------------------------------------|:-------:|:-------------:|
|  page    | No       | Page number.                          | 1       | `page=1`      |
| per_page | No       | Results per page.                     |  10     | `per_page=10` |

**Example Response:**

```json
[
    {
        "id": 1,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "This is my bio.",
        "year": 2021,
        "group": 1,
    },
    {
        "id": 3,
        "username": "johndoe2",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "This is my bio.\r\nGo Blue!",
        "year": 2022,
        "group": 1,
    },
]
```

---

## Workouts

### Workout Model:

| Name | Type | Description |
|:-----|:----:|:------------|
| id | integer | Unique workout identifier. |
| title | char | Title of the workout. |
| description | text | Workout description. |
| category | char | unique category identifier. |
| owner | integer | user_id of owner. |


```python
GET api/v1/workouts/
```

**Description** : Returns a list of Workout objects

**Auth required** : YES

**Permissions required** : None

### Parameters

|  Name    | Required |              Description              | Default |    Example    |
|:---------|:--------:|:--------------------------------------|:-------:|:-------------:|
|  page    | No       | Page number.                          | 1       | `page=1`      |
| per_page | No       | Results per page.                     |  10     | `per_page=10` |
|  type    | No       | Returns workouts of specified type.   | None    | `type=1`      |

**Example Response:**

```json
[
    {
        "id": 1,
        "title": "4x400m",
        "description": "4 min rest between reps. I don't reccomend wearing spikes for these.",
        "category": "T",
        "owner": 1,
    },
    {
        "id": 2,
        "title": "30-30s",
        "description": "200s in 30 sec with 30 sec rest. I usually do 6-8 of them. If you arent in shape these are pretty tough so you can aim for a longer time like all under 35s for example. If you aren't hitting the time either make it higher or take a 5 min rest halfway through.",
        "category": "T",
        "owner": 1,
    },
]
```

---

```python
POST api/v1/workouts/
```

**Description** : Creates a new workout

**Auth required** : YES

**Permissions required** : None

**Parameters:** None

---

```python
GET api/v1/workouts/{workout_id}/
```

**Description** : Returns a Workout object

**Auth required** : YES

**Permissions required** : None

**Parameters:** None

**Example Response:**

```json
{
    "id": 1,
    "title": "4x400m",
    "description": "4 min rest between reps. I don't reccomend wearing spikes for these.",
    "category": "T",
    "owner": 1,
}
```

---

```python
DELETE api/v1/workouts/{workout_id}/
```

**Description** : Deletes a workout

**Auth required** : YES

**Permissions required** : logged in user is Owner or Admin

**Parameters:** None

---

```python
PATCH api/v1/workouts/{workout_id}/
```

**Description** : Modifies a Workout

**Auth required** : YES

**Permissions required** : logged in user is Owner

**Parameters:** None

**Example Response:**

```json
{
    "id": 1,
    "title": "4x400m",
    "description": "4 min rest between reps. I don't reccomend wearing spikes for these.",
    "category": "T",
    "owner": 1,
}
```

---

## Activities

### Activity Model:

| Name | Type | Description |
|:-----|:----:|:------------|
| id | integer | unique key for every Activity. |
| user | integer | user_id of the User who completed the workout. |
| workout | integer | workout_id for the corresponding Workout. |
| time | DateTime | time activity was completed. |
| comment | text | comment about the activity. |

```python
POST api/v1/activities/
```

**Description** : Creates a new activity for the logged in user

**Auth required** : YES

**Permissions required** : None

### Parameters

|    Name     | Required |                    Description                  | Default |    Example    |
|:------------|:--------:|:------------------------------------------------|:-------:|:-------------:|
| new_workout |   No     | Indicates if a new workout needs to be created. | 0       | `new_workout=1`      |

---

```python
GET api/v1/activities/
```

**Description** : Returns a list of Activity summaries.

**Auth required** : YES

**Permissions required** : None

### Parameters

|  Name    | Required |              Description              | Default |    Example    |
|:---------|:--------:|:--------------------------------------|:-------:|:-------------:|
|  page    | No       | Page number.                          | 1       | `page=1`      |
| per_page | No       | Results per page.                     |  10     | `per_page=10` |
| filter   | No       | Criteria to filter on ("group" or the workout type) | None | `filter=group` |

**Example Response:**

```json
[
    {
        "id": 1,
        "user": 1,
        "workout": 2,
        "time": "2020-06-21T19:46:45.315Z",
        "comment": "This is a comment.",
        "workout_data": {
            "id": 2,
            "title": "4x400m",
            "description": "4 min rest between reps. I don't reccomend wearing spikes for these.",
            "category": "T",
            "owner": 1,
        },
    },
    {
        "id": 2,
        "user": 1,
        "workout": 2,
        "time": "2020-06-22T19:46:45.315Z",
        "comment": "This is another comment.",
        "workout_data": {
            "id": 2,
            "title": "4x400m",
            "description": "4 min rest between reps. I don't reccomend wearing spikes for these.",
            "category": "T",
            "owner": 1,
        },
    },
]
```

---

```python
GET api/v1/activities/{activity_id}/
```

**Description** : Returns an Activity object

**Auth required** : YES

**Permissions required** : None

**Parameters:** None

**Example Response:**

```json
{
    "id": 1,
    "user": 1,
    "workout": 2,
    "time": "2020-06-21T19:46:45.315Z",
    "comment": "This is a comment.",
}
```

---

```python
DELETE api/v1/activities/{activity_id}/
```

**Description** : Deletes an Activity object

**Auth required** : YES

**Permissions required** : Admin or Owner

**Parameters:** None

---

```python
GET api/v1/activities/{activity_id}/comments/
```

**Description** : Returns a list of Comment objects associated with specified activity.

**Auth required** : YES

**Permissions required** : None

**Parameters:** None

**Example Response:**

```json
[
    {
        "id": 01,
        "activity": 01,
        "user": 01,
        "time": "2020-06-21T19:46:45.315Z",
        "text": "This is a comment.",
    },
    {
        "id": 02,
        "activity": 01,
        "user": 01,
        "time": "2020-06-21T19:47:01.826Z",
        "text": "This is another comment.",
    },
]
```

---

## Comments

### Comment Model:

| Name | Type | Description |
|:-----|:----:|:------------|
| id | integer | unique key for each comment.|
| activity | integer | activity_id for the activity the comment was for. |
| user | integer | user_id for user making the comment. |
| time | DateTime | time when the comment was created. |
| text | text | the body of the comment. |

```python
GET api/v1/comments/
```

**Description** : Returns a list of comment objects. If there is a next page, then "next" will contain it, otherwise "next" will not exist.

**Auth required** : YES

**Permissions required** : None

### Parameters

|  Name    | Required |              Description              | Default |    Example    |
|:---------|:--------:|:--------------------------------------|:-------:|:-------------:|
|  page    | No       | Page number.                          | 1       | `page=1`      |
| per_page | No       | Results per page.                     |  10     | `per_page=10` |
|  user    | No       | Returns comments of only one user.    | None    | `user=1`      |

**Example Response:**

```json
{
    "comments": [
        {
            "id": 01,
            "activity": 01,
            "user": 01,
            "time": "2020-06-21T19:46:45.315Z",
            "text": "This is a comment.",
        },
        {
            "id": 02,
            "activity": 01,
            "user": 01,
            "time": "2020-06-21T19:47:01.826Z",
            "text": "This is another comment.",
        },
    ],
    "next": 2,
}

```

---

```python
POST api/v1/comments/
```

**Description** : Creates a Comment object

**Auth required** : YES

**Permissions required** : None

**Parameters:** None

**Example:**

```bash
curl --header "Content-type: application/json" \
  --request POST \
  --data '{"activity": [[activity_id]], "text":"[[text goes here]]"}' \
  http://localhost:8000/api/comments/
```

---

```python
PATCH api/v1/comments/{comment_id}/
```

**Description** : Modifies a Comment object

**Auth required** : YES

**Permissions required** : None

**Parameters:** None

**Example:**

```bash
curl --header "Content-type: application/json" \
  --request PATCH \
  --data '{"text":"[[text goes here]]"}' \
  http://localhost:8000/api/comments/{comment_id}/
```

**Example Response:**

```json
{
    "id": 01,
    "activity": 01,
    "user": 01,
    "time": "2020-06-21T19:46:45.315Z",
    "text": "This is a comment.",
}
```

---

```python
DELETE api/v1/comments/{comment_id}/
```

**Description** : Deletes a Comment object

**Auth required** : YES

**Permissions required** : Owner or Admin

**Parameters:** None


## Suggestions

### Suggestion Model:

| Name |  Type   | Description |
|:-----|:-------:|:------------|
|  id  | integer | unique identifier for each suggestion |
| group_id | integer | group identifier |
| workout_id | integer | workout identifier |
| date | Date | day the suggestion is for |

```python
GET api/v1/suggestions/
```

**Description** : Returns the suggested workout for the given date and group.

**Auth required** : YES

**Permissions required** : None

### Parameters

|  Name  | Required |              Description              | Default |    Example    |
|:-------|:--------:|:--------------------------------------|:-------:|:-------------:|
| group  | No       | group_id of the group                 | 1       | `group=1`      |
|  date  | No       | Date of the suggestion                |  today  | `date=2020-07-14` |

**Example Response:**

```json
{
    "id": 1,
    "title": "4x400m",
    "description": "4 min rest between reps. I don't reccomend wearing spikes for these.",
    "category": "T",
    "owner": 1,
}
```

---

```python
POST api/v1/suggestions/
```

**Description** : Returns the suggested workout for the given date and group.

**Auth required** : YES

**Permissions required** : Admin

**Parameters:** None

**Example Request:**

```json
{
    "group": 1,
    "workout": 2,
    "date": "2020-07-14",
}
```

**Success Response:** 201 ACCEPTED

---

```python
GET api/v1/suggestions/{suggestion_id}/
```

**Description:** Returns the suggestion object with a summary of the workout.

**Auth required:** YES

**Permissions required:** None

**Parameters:** None

**Example Response:**

```json
{
    "id": 1,
    "group": 2,
    "date": "2020-07-14",
    "workout": {
        "id": 1,
        "title": "4x400m",
        "description": "4 min rest between reps. I don't reccomend wearing spikes for these.",
        "category": "T",
        "owner": 1,
    }

}
```

---

```python
DELETE api/v1/suggestions/{suggestion_id}/
```

**Description:** Deletes the suggestion object with suggestion_id.

**Auth required:** YES

**Permissions required:** Admin

**Parameters:** None

**Success Response:** 204 NO CONTENT

---

## Memberships

### Membership Model:

| Name |  Type   | Description |
|:-----|:-------:|:------------|
| id | integer | unique identifier for each relationship |
| group_id | integer | group identifier |
| user_id | integer | user identifier |

user_id must be unique across all membership entries.

```python
POST api/v1/membership/
```

**Description:** Allows users to update their membership status. Will overwrite existing entry if exists.

**Auth required:** YES

**Permissions required:** None

### Parameters:

|  Name | Required |              Description              |  Example    |
|:------|:--------:|:--------------------------------------|:-----------:|
| group |  yes     | The group_id for the group you would like to join. | `group=3` |

**Example Responses:**
| code | meaning |
|:----:|:--------|
| 201  | Success |
| 400 | missing or incorrect group_id |

---

```python
GET api/v1/membership/
```

**Description:** Returns the group_id for the logged in user.

**Auth required:** YES

**Permissions required:** None

**Parameters:** None

**Example Responses:**
| code | meaning |
|:----:|:--------|
| 200  | Success |
| 400 | user is not in a group |
| 403 | not authenticated |

**Success Response:**

```json
{
    "user": 1,
    "group": 1,
}
```

