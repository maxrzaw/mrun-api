# API Endpoints
## Table of Contents
- [Users](#users)
- [Groups](#groups)
- [Workouts](#workouts)
- [Activities](#activities)
- [Comments](#comments)
## Users

```python
GET api/v1/users/
```
**Description** : Returns a list of users

**Auth required** : YES

**Permissions required** : None

### Parameters
|  Name | Required |            Description            | Default | Example |
|:------|:--------:|:----------------------------------|:-------:|:-------:|
| group | No       | Filter by groupID                 | None    | `1`     |
| year  | No       | Filter by graduation year         | None    | `2021`  |

---

```python
GET api/v1/users/{userID}/
```
**Description** : Returns user object with `userID`

**Auth required** : YES

**Permissions required** : None

### Parameters
None

---

```python
GET api/v1/users/{userID}/activities/
```
**Description** : 

**Auth required** : YES

**Permissions required** : 

### Parameters
|  Name    | Required |              Description              | Default | Example |
|:---------|:--------:|:--------------------------------------|:-------:|:-------:|
|  type    | No       | Returns activities of specified type. | None    | `type=1` |
|  page    | No       | Page number.                          | 1       | `page=1`      |
| per_page | No       | Results per page.                     |         | `per_page=10`      |

---

```python
POST api/v1/users/{userID}/activities/
```
**Description** : Creates a new activity

**Auth required** : YES

**Permissions required** : Logged in user is userID

### Parameters
|  Name | Required |            Description            | Default | Example |
|:------|:--------:|:----------------------------------|:-------:|:-------:|
|       |          |                                   |         | ``      |
|       |          |                                   |         | ``      |
|       |          |                                   |         | ``      |


## Groups
## Workouts
## Activities
## Comments





# Template:
---

```python
GET POST PATCH DELETE api/v1/
```
**Description** : 

**Auth required** : YES/NO

**Permissions required** : 

### Parameters
|  Name | Required |            Description            | Default | Example |
|:------|:--------:|:----------------------------------|:-------:|:-------:|
|       |          |                                   |         | ``      |
|       |          |                                   |         | ``      |
|       |          |                                   |         | ``      |
