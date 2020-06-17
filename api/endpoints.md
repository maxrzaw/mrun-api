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
| group | No       | Filter by group_id                | None    | `group=1`     |
| year  | No       | Filter by graduation year         | None    | `year=2021`  |

---

```python
GET api/v1/users/{user_id}/
```
**Description** : Returns user object with `user_id`

**Auth required** : YES

**Permissions required** : None

### Parameters
None

---

```python
GET api/v1/users/{user_id}/activities/
```
**Description** : Returns a list of Activity objects for user with user_id

**Auth required** : YES

**Permissions required** : Signed in

### Parameters
|  Name    | Required |              Description              | Default |    Example    |
|:---------|:--------:|:--------------------------------------|:-------:|:-------------:|
|  type    | No       | Returns activities of specified type. | None    | `type=1`      |
|  page    | No       | Page number.                          | 1       | `page=1`      |
| per_page | No       | Results per page.                     |  10     | `per_page=10` |
| sort     | No       | Sort by date ascending or descending. | desc    | `sort=asc`    |

---

```python
GET api/v1/users/{user_id}/workouts/
```
**Description** : Returns workouts for user_id

**Auth required** : YES

**Permissions required** : None

[//]: # (Might change this to following later on)

### Parameters
|  Name    | Required |              Description              | Default |    Example    |
|:---------|:--------:|:--------------------------------------|:-------:|:-------------:|
|  type    | No       | Returns workouts of specified type.   | None    | `type=1`      |
|  page    | No       | Page number.                          | 1       | `page=1`      |
| per_page | No       | Results per page.                     |  10     | `per_page=10` |

---

## Groups

```python
GET api/v1/groups/
```
**Description** : Returns a list of group objects

**Auth required** : YES

**Permissions required** : None

### Parameters
|  Name    | Required |              Description              | Default |    Example    |
|:---------|:--------:|:--------------------------------------|:-------:|:-------------:|
|  page    | No       | Page number.                          | 1       | `page=1`      |
| per_page | No       | Results per page.                     |  10     | `per_page=10` |

---

```python
POST api/v1/groups/
```
**Description** : Create a group

**Auth required** : YES

**Permissions required** : Admin

### Parameters
None

---

```python
PATCH api/v1/groups/
```
**Description** : Modify a group

**Auth required** : YES

**Permissions required** : Admin

### Parameters
None

---

```python
DELETE api/v1/groups/
```
**Description** : Removes a group

**Auth required** : YES

**Permissions required** : Admin

### Parameters
None

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

---

## Workouts

```python
GET api/v1/workouts/
```
**Description** :

**Auth required** : YES

**Permissions required** : None

### Parameters
|  Name    | Required |              Description              | Default |    Example    |
|:---------|:--------:|:--------------------------------------|:-------:|:-------------:|
|          |          |                                       |         | ``            |
|          |          |                                       |         | ``            |
|          |          |                                       |         | ``            |

---

```python
POST api/v1/workouts/
```
**Description** :

**Auth required** : YES

**Permissions required** : None

### Parameters
|  Name    | Required |              Description              | Default |    Example    |
|:---------|:--------:|:--------------------------------------|:-------:|:-------------:|
|          |          |                                       |         | ``            |
|          |          |                                       |         | ``            |
|          |          |                                       |         | ``            |

---

```python
DELETE api/v1/workouts/{workout_id}
```
**Description** : Deletes a workout

**Auth required** : YES

**Permissions required** : logged in user is Owner or Admin

### Parameters
None

---

## Activities

```python
POST api/v1/activities/
```
**Description** : Creates a new activity

**Auth required** : YES

**Permissions required** : None

### Parameters
None

---

## Comments





# Template:

```python
GET POST PATCH DELETE api/v1/
```
**Description** :

**Auth required** : YES/NO

**Permissions required** :

### Parameters
|  Name    | Required |              Description              | Default |    Example    |
|:---------|:--------:|:--------------------------------------|:-------:|:-------------:|
|          |          |                                       |         | ``            |
|          |          |                                       |         | ``            |
|          |          |                                       |         | ``            |

---
