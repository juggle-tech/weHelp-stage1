# Week5 Assignment

## Task 2

**SQL：**

```sql
CREATE DATABASE website;

CREATE TABLE member(
  id INT UNSIGNED NOT NULL AUTO_INCREMENT, 
  name VARCHAR(254) NOT NULL, 
  email VARCHAR(254) NOT NULL, 
  password VARCHAR(254) NOT NULL, 
  follower_count INT UNSIGNED NOT NULL DEFAULT 0, 
  time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
  PRIMARY KEY(id)
);
```

**Screenshots：**

![task2-1](imgs/T2-1.png)
![task2-2](imgs/T2-2.png)

---

## Task 3

**SQL：**

```sql
INSERT INTO member(name, email, password) VALUES('test', 'test@test.com', 'test');

SELECT * FROM member;

SELECT * FROM member ORDER BY time DESC;

SELECT * FROM member ORDER BY time DESC LIMIT 3 OFFSET 1;

SELECT * FROM member WHERE email = 'test@test.com';

SELECT * FROM member WHERE name LIKE '%es%';

SELECT * FROM member WHERE email = 'test@test.com' AND password = 'test';

UPDATE member SET name = 'test2' WHERE email = 'test@test.com';
```

**Screenshots：：**

![task3-1](imgs/T3-1.png)
![task3-2](imgs/T3-2.png)
![task3-3](imgs/T3-3.png)
![task3-4](imgs/T3-4.png)
![task3-5](imgs/T3-5.png)
![task3-6](imgs/T3-6.png)
![task3-7](imgs/T3-7.png)
![task3-8](imgs/T3-8.png)

---

## Task 4

**SQL：**

```sql
SELECT COUNT(*) FROM member;

SELECT SUM(follower_count) FROM member;

SELECT AVG(follower_count) FROM member;

SELECT AVG(follower_count) FROM (SELECT * FROM member ORDER BY follower_count DESC LIMIT 2) AS T2;
```

**Screenshots：**

![task4-1](imgs/T4-1.png)
![task4-2](imgs/T4-2.png)
![task4-3](imgs/T4-3.png)
![task4-4](imgs/T4-4.png)

---

## Task 5

**SQL：**

```sql
CREATE TABLE message(
  id INT UNSIGNED NOT NULL AUTO_INCREMENT, 
  member_id INT UNSIGNED NOT NULL, 
  content text NOT NULL, 
  like_count INT UNSIGNED NOT NULL DEFAULT 0, 
  time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
  PRIMARY KEY(id), 
  FOREIGN KEY (member_id) REFERENCES member(id)
);

SELECT mes.*, mem.name FROM message AS mes LEFT JOIN member AS mem ON mes.member_id = mem.id;

SELECT mes.*, mem.name FROM message AS mes LEFT JOIN member AS mem ON mes.member_id = mem.id WHERE mem.email = 'test@test.com';

SELECT mem.email, AVG(mes.like_count) FROM message AS mes LEFT JOIN member AS mem ON mes.member_id = mem.id WHERE mem.email = 'test@test.com';  

SELECT mem.email, AVG(mes.like_count) FROM message AS mes LEFT JOIN member AS mem ON mes.member_id = mem.id GROUP BY mem.email;
```

**Screenshots：**

![task5-1](imgs/T5-1.png)
![task5-2](imgs/T5-2.png)
![task5-3](imgs/T5-3.png)
![task5-4](imgs/T5-4.png)
![task5-5](imgs/T5-5.png)