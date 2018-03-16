# Bookmark App

## 북마크 앱

https://getpocket.com/



## **GetPocket**?

* Pocket 앱은 iOS (아이폰/아이패드), 안드로이드, 맥, 웹 등 많은 플랫폼을 지원



## Pocket 사용!

글을 읽다가 어떠한 이유로 나중에 읽어야 할때...



![GetPocket](https://ablex.ru/wp-content/uploads/2015/01/screen-shot-2012-11-27-at-8-50-24-pm.png)



![img](https://lh3.googleusercontent.com/huMFUpe1bw-m1WHj77J5oKmcFJO37D9fTLwTKZDfla_XPISw0DjLTIBfdboz3wmIasUbKTDG=w640-h400-e365)



## 구현 기능

북마크 등록

북마크 삭제

북마크 즐겨찾기

북마크 리스트











## Model

| 필드명      | 타입           | 제약 조건          | 설명        |
| ----------- | -------------- | ------------------ | ----------- |
| id          | Integer        | PK, Auto Increment | 기본 키     |
| url         | UrlField()     |                    | URL         |
| domain      | UrlField()     | Blank              | domain URL  |
| title       | CharField(100) | Blank              | 제목        |
| description | CharField(500) | Blank              | 요약        |
| favicon     | TextField()    | Blank              | 파비콘      |
| image       | TextField()    | Blank              | 대표 이미지 |
| star        | BooleanField   | delfault = false   | 즐겨찾기    |
| created     | DateTimeField  | auto_now_add       | 생성 날짜   |



## API

| url 패턴           | 뷰이름   | Payload                                                  |
| ------------------ | -------- | -------------------------------------------------------- |
| bookmark/          | 리스트   | [{ id, url, domain, title, description, img, created },] |
| bookmark/99        | 상세     | { id, url, domain, title, description, img, created }    |
| bookmark/create/   | 생성     | url                                                      |
| bookmark/delete/99 | 삭제     | { id }                                                   |
| bookmark/update/99 | 즐겨찾기 | { id, star: true }                                       |

추가 - tag, search