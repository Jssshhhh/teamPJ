from PIL import Image

# 로컬 이미지 파일 경로
lg_image_path = "./image/lg-twins.jpg"  # LG 트윈스 이미지 경로
doosan_image_path = "./image/doosan-bears.jpg"  # 두산 베어스 이미지 경로

try:
    lg_image = Image.open(lg_image_path).convert("RGBA")  # RGBA 모드로 변환
    doosan_image = Image.open(doosan_image_path).convert("RGBA")  # RGBA 모드로 변환
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)

# 이미지 크기 조정
lg_image = lg_image.resize((100, 100), Image.LANCZOS)
doosan_image = doosan_image.resize((100, 100), Image.LANCZOS)

# 새로운 배경 이미지 생성
background = Image.new('RGBA', (200, 100), (255, 255, 255, 0))  # 투명 배경

# 이미지를 배경에 추가
background.paste(lg_image, (0, 0), lg_image)  # lg_image를 붙임
background.paste(doosan_image, (100, 0), doosan_image)  # doosan_image를 붙임

# 결과 이미지 저장
combined_image_path = "combined_logo.png"
background.save(combined_image_path)

print("Combined logo saved as 'combined_logo.png'.")