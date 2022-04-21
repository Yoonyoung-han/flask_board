# 1. 실행 순서
 `1. Flask run 전에 Flask 환경 변수 설정을 해줘야한다.`  
 ` - set FLASK_APP=pybo -> pybo.py를 의미한다. 가상환경에서 안먹힐때는 export FLASK_APP=pybo 하면 잘된다.`  
 `- set FLASK_ENV=development 으로 개발환경으로 만들자 `


`2. flask run  하면 잘 실행된다.`

# 2. 환경 구성
`1. mongoDB 설치 후, sample_db의 이름으로 database를 생성한다.`   
`2. mongoDB에 answer,comment,question,user 컬렉션을 옵션없이 각각 생성한다.`  
`3. redis 설치 (로그인을 위해 필요한 작업)`  
```
공홈에서 stable tar파일 다운 받기
$ tar xvzf redis-stable.tar.gz
$ cd redis-stable
$ make
$ redis-server # 서버시작
$ redis-cli ping ==>응답 PONG
$ redis-cli shutdown # 서버 정지
```  
` * mongodb 비정상 종료 후 다시 시작할 때 *`  
```
$ sudo rm -rf /tmp/mongodb-27017.sock
$ sudo service mongod start
$ sudo service mongod status
/etc/mongod.conf 에 security 부분 주석처리 후 restart

```
# 3. docker-compose 관련 정리
`1. image 전체 삭제는 sudo docker-compose down -v --rmi all --remove-orphans 로 한다.`  
`2. 빌드 및 올리는 것은 sudo docker-compose up 한다.`  