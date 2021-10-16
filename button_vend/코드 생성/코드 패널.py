import requests, os, time
from requests.models import codes

try:
    gen_date = int(input('생성 기간 : '))
    if 1 <= gen_date <= 99999: 
        gen_number = int(input('생성 개수 : '))
    else:
        os.system('cls')
        print('1~99999의 기간을 입력해주세요.')
except:
    os.system('cls')
    print('올바른 수를 입력해주세요.')

os.system('cls')
for n in range(gen_number):
    res = requests.post('도메인:5050/licensegen', json={
        'license_length': str(gen_date)
    })
    code = res.json()['code']
    if code == '등록되지 않은 아이피':
        print('등록되지 않은 아이피입니다.')
        d = False
        break
    else:
        print(code)
        open(f'{gen_date}일 라이센스.txt', 'a').write(code + '\n')
        d = True
if not d == False:
    print(f'\n코드 생성이 끝났습니다. {gen_date}일 라이센스.txt 파일을 확인해주세요.')
time.sleep(60)