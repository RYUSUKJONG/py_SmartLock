import RPi.GPIO as GPIO  
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from time import sleep

#서보모터,led,기울기 센서 GPIO 보드번호
servo=37
inled =35
outled =36
tilt_pin=38

GPIO.setmode(GPIO.BOARD)#gpio 모드를 보드번호 사용
GPIO.setwarnings(False)
GPIO.setup(servo, GPIO.OUT)#서보모터을 출력핀으로 설정
GPIO.setup(inled,GPIO.OUT)#led을 출력핀으로 설정
GPIO.setup(outled,GPIO.OUT)#led을 출력핀으로 설정
GPIO.setup(tilt_pin, GPIO.IN)#기울기를 입력핀으로 설정

p = GPIO.PWM(servo, 50)#서보모터를 펄스 폭 변조로 제어


#Firebase database 인증
#Firebase에서 생성한 인증키를 통하여 서비스계정 인증
#smartlock123.json 파일에는 firebase 서비스 계정과 관련된 모든 정보 포함 (프로젝트id,프로젝트keyid,클라이언트id,email,인증uri,토큰uri 등..)
cred = credentials.Certificate('smartlock123.json')
#Firebase database 앱 초기화
firebase_admin.initialize_app(cred,{'databaseURL':'https://smartlock123-7aa90.firebaseio.com/'})



ref = db.reference('lockcommand')
lc=ref.get()
print(lc)
        
        
if __name__ == '__main__':
    p.start(0)#서보모터 동작
    while True:
        # Initialize the keypad class
        ref = db.reference('lockcommand')#파이어베이스로부터 lockcommand지정
        lockcommand=ref.get()#읽은 lockcommand값을 변수에 저장
        print("lockcommand"+lockcommand)
        
        ref = db.reference('led')#파이어베이스로부터 led지정
        led=ref.get()#읽은 led값을 변수에 저장
        print("led"+led)
        
        ref = db.reference('tilt')#파이어베이스로부터 tilt지정
        tilt=ref.get()#읽은 tilt값을 변수에 저장
        print("tilt"+tilt)
        
		#led 값이 1일때
        if led == '1' :
            GPIO.output(inled,True)#led ON
        #led 값이 0일때
		if led == '0' :
            GPIO.output(inled,False)#led OFF
        
        
        
		#lockcommand 값이 1일때
		#서보모터를 90도 움직인다, lockstae값을 1로 db에 업데이트, outled ON
        if lockcommand == '1' :
            p.ChangeDutyCycle(7.5)
            ref = db.reference()
            ref.update({'lockstate':'1'})
            GPIO.output(outled,True)
            time.sleep(1)
            
        #lockcommand 값이 1일때
		#서보모터를 -90도 움직인다, lockstae값을 0로 db에 업데이트, outled OFF    
        if lockcommand == '0' :
            ref = db.reference()
            ref.update({'lockstate':'0'})
            p.ChangeDutyCycle(2.5)
            GPIO.output(outled,False)
            time.sleep(1)
            
        #기울기 센서에 입력값이 있을때
		#db의 tilt 값을 1로 업데이트 하고 입력값이 없을때는 0으로 업데이트 한다
        if GPIO.input(tilt_pin) :
            print("tilt")
            ref = db.reference()
            ref.update({'tilt':'1'})
        else :
            ref = db.reference()
            ref.update({'tilt':'0'})
            
       
        
            
        
        
            
    p.stop()
            

