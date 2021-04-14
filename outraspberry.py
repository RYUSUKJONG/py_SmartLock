import RPi.GPIO as GPIO  
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from keypad import*

#Firebase database 인증
#Firebase에서 생성한 인증키를 통하여 서비스계정 인증
#smartlock123.json 파일에는 firebase 서비스 계정과 관련된 모든 정보 포함 (프로젝트id,프로젝트keyid,클라이언트id,email,인증uri,토큰uri 등..)
cred = credentials.Certificate('smartlock123.json')
#Firebase database 앱 초기화
firebase_admin.initialize_app(cred,{'databaseURL':'https://smartlock123-7aa90.firebaseio.com/'})

buzzer=16 #부저 GPIO 보드번호
outled=36
GPIO.setmode(GPIO.BOARD)#gpio 모드를 보드번호 사용
GPIO.setup(buzzer, GPIO.OUT)#부저핀을 출력핀으로 설정
GPIO.setup(outled, GPIO.OUT

scale = [ 261, 294, 329, 349, 392, 440, 493, 523 ]#부저 음 도레미파솔라시도
list = [4, 4, 5, 5, 4, 4, 2, 4, 4, 2, 2, 1]#비행기 음

wrong=0;#비밀번호 입력 실패시 카운트할 변수

b = GPIO.PWM(buzzer, 100)

if __name__ == '__main__':
    while True:
        ref = db.reference('password')#파이어베이스로부터 password값지정
        password = ref.get()#읽은 password값을 변수에 저장
        print(password)
        
		pwd = [] #키페드로 부터 입력받은 값을 저장할 공간
        kp = keypad()
        
       
        for i in range(6): #6자리를 입력받은 pwd에 저장
            digit = None
            while digit == None:
                digit = kp.getKey()
            pwd.append(digit)
            time.sleep(0.4)
     
        # Check digit code
        print(pwd)
        str1 = "".join(map(str,pwd))#pwd를 문자열로 변환하여 저장
        print(str1)
        
        if password==str1 : #입력받은password와 데이터베이스로부터 읽은 password가 맞을때
            ref = db.reference()
            ref.update({'lockcommand':'0'})#파이어베이스의 lockcommand 값 0으로 업데이트
            print("update lockcommand 0")
            wrong=0#wrong값 초기화
            
			#부저로부터 열리는 소리 출력 
            b.start(100)
            b.ChangeDutyCycle(90)
            b.ChangeFrequency(261)
            time.sleep(0.5)
            b.ChangeFrequency(329)
            time.sleep(0.5)
            b.stop()

            
        else : # 비밀번호 틀렸을 때
            wrong+=1 #wrong값 1 증가 
            ref = db.reference() 
            ref.update({'lockcommand':'1'})#파이어베이스의 lockcommand 값 1으로 업데이트
            print("update lockcommand 1")
            print(wrong)
			
			#부저로부터 경고음 소리 출력
            b.start(100)
            b.ChangeDutyCycle(90)
            b.ChangeFrequency(523)
            time.sleep(0.5)
            
            b.stop()
            
            
            if wrong==3 : #3번 틀렸을때
				ref = db.reference()
                ref.update({'buzzer':'1'})#파이어베이스의  buzzer 값 1으로 업데이트
                  
                #부저로 부터 경고음 출력
                b.start(100)
                b.ChangeDutyCycle(90)
                    
                for i in range(12):
					print(i+1)
                    b.ChangeFrequency(scale[list[i]])
                    if i == 6 :
						time.sleep(1)
                    else :
						time.sleep(0.5)
				b.stop()
				
             
            
            
    #GPIO 모듈의 점유 리소스를 해제        
	GPIO.cleanup()		
            