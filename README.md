# Sparta Market
중고거래 플랫폼

## Introduction
**Sparta Market** is a second-hand marketplace platform where users can buy and sell used goods. The platform provides features for listing items, managing transactions, and communicating with buyers and sellers. This project was developed using Django framework.

## Duration
24.08.20 - 24.08.26
    
## TechStack
- :art: **Front-End**

  - **Language**
    - ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

  - **Framework / Library**
    - ![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)

- :computer: **Back-End**

  - **Language**
    - ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white)

  - **Framework**
    - ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)

## Model
ERD 첨부예정.

## Setup

To set up and run the project, follow these steps:

1. Clone the project repository:

    ```bash
    git clone https://github.com/kimwoolina/Sparta_market/
    ```

2. Navigate to the project directory:

    ```bash
    cd /Users/YourPC/Your_Cloned_Folder/Sparta_market/spartamarket
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Run the development server:

    ```bash
    python manage.py runserver
    ```

6. Open your browser and visit:

    [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Service
**홈 화면** 'http://127.0.0.1:8000/index/'
<img width="1439" alt="스크린샷 2024-08-26 오후 5 41 33" src="https://github.com/user-attachments/assets/8f103c42-6b52-49bd-a7ed-7eb9e838c8f1">

<br>
**물품 목록 화면** 'http://127.0.0.1:8000/products/'
<img width="1423" alt="스크린샷 2024-08-26 오후 5 45 32" src="https://github.com/user-attachments/assets/d1210f69-f1b5-4fd9-a41e-7ecc5f77ac53">
<img width="1427" alt="스크린샷 2024-08-26 오후 5 45 53" src="https://github.com/user-attachments/assets/2b081b4c-333d-4246-950a-72b8a4372785">
<br>

**최신순 정렬 기능** 'http://127.0.0.1:8000/products/products/?sort=latest'
<img width="1419" alt="스크린샷 2024-08-26 오후 5 47 58" src="https://github.com/user-attachments/assets/1e052a53-736c-4486-8cf1-dbe1b2a2f48b">
<br>

**인기순 정렬 기능** 'http://127.0.0.1:8000/products/products/?sort=popular'
<img width="1427" alt="스크린샷 2024-08-26 오후 5 48 48" src="https://github.com/user-attachments/assets/05482d26-7289-400e-8fb0-fd7be4060d85">
<br>

**회원가입 화면** 'http://127.0.0.1:8000/accounts/signup/'
<img width="1440" alt="스크린샷 2024-08-26 오후 5 56 51" src="https://github.com/user-attachments/assets/88e1c67a-ec8b-4c32-a6fc-2fb3b03d8c69">
<br>

**로그인 화면** 'http://127.0.0.1:8000/accounts/login/'
<img width="1432" alt="스크린샷 2024-08-26 오후 5 47 11" src="https://github.com/user-attachments/assets/d5021db6-024e-4958-8011-c5de46d8afe1">
<br>

**마이페이지** 'http://127.0.0.1:8000/users/profile/<username>/'
<img width="1377" alt="스크린샷 2024-08-26 오후 5 51 09" src="https://github.com/user-attachments/assets/bf99bff5-1b69-4817-bdd3-efbd431002d8">
<br>

**내 매물목록 페이지** 'http://127.0.0.1:8000/users/<username>/products/'
<img width="1432" alt="스크린샷 2024-08-26 오후 5 53 29" src="https://github.com/user-attachments/assets/2a4dbde6-411f-4c17-a289-c221f322a1b9">
<br>

**관심목록 페이지** 'http://127.0.0.1:8000/users/admin/liked-products/'
<img width="1346" alt="스크린샷 2024-08-26 오후 5 54 28" src="https://github.com/user-attachments/assets/4ade0263-b495-4a55-b1bc-a7790b45d046">
<br>

**회원 정보 수정 페이지** 'http://127.0.0.1:8000/accounts/update/'
<img width="1408" alt="스크린샷 2024-08-26 오후 5 55 03" src="https://github.com/user-attachments/assets/66784b20-4084-4be1-8566-9e04358feb14">
<br>
 
**검색 기능** 'http://127.0.0.1:8000/products/search/?query=<검색어>'
<img width="1437" alt="스크린샷 2024-08-26 오후 5 57 24" src="https://github.com/user-attachments/assets/dd1da779-bf9d-4294-a78b-5bf27760b2ce">



