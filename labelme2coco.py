import os 
import json
import glob

#필수요소 - 이미지 데이터(고유 id, 파일 이름), 객체 ㅋ테고리, ,주석

def labelme_to_coco(data_path, output_json):
    # 데이터 경로 내의 모든 JSON 파일을 찾기
    data = glob.glob(os.path.join(data_path, '*.json'))
    print("len:", len(data))

    # COCO 형식의 기본 구조 정의
    make_coco = {'images': [], 'annotations': [], 'categories': []}

    # 범주 ID를 추적할 사전
    category_id_dict = {}
    annotation_id = 1

    # 인덱스와 경로 받기
    for img_id, json_file in enumerate(data):
        with open(json_file, 'r') as f:
            load_json = json.load(f)
            print(img_id[1])

        # 이미지에 대한 정보 추가
        image_info = {
            'license': 0,
            'file_name': os.path.basename(json_file).replace('.json', '.jpg'),  # 규칙이라 jpg로 확장자를 변경해줌
            'height': load_json['imageHeight'], 
            'width': load_json['imageWidth'],
            'id': img_id
        }
        make_coco['images'].append(image_info) # 이미지 정보 추가

        for shape in load_json['shapes']:
            label = shape['label']      #클래스 이름
            if label not in category_id_dict:       # 라벨 있는 지 확인하여 중복 라벨 방지 고유 카테고리 할당
                category_id = len(category_id_dict) + 1                 #등록 카테고리에 1 더해서 객체 카테고리 추가
                category_id_dict[label] = category_id               #같은 카테고리여도 동일한 카테고리 추가 
                make_coco['categories'].append({'id': category_id, 'name': label})         

            x1, y1 = min(point[0] for point in shape['points']), min(point[1] for point in shape['points'])    
            x2, y2 = max(point[0] for point in shape['points']), max(point[1] for point in shape['points'])
            width, height = x2 - x1, y2 - y1
            area = width * height

            # 주석 정보 추가
            annotation_info = {
                'id': annotation_id,
                'image_id': img_id,
                'category_id': category_id_dict[label],
                'area': area,
                'bbox': [x1, y1, width, height],
                'iscrowd': 0,
                'segmentation': [point for point in shape['points']]
            }
            make_coco['annotations'].append(annotation_info)
            annotation_id += 1

    # COCO 형식의 JSON 파일 저장
    with open(output_json, 'w') as f:
        json.dump(make_coco, f, indent=4) # 들여쓰기 해서 보기 쉽게 함

if __name__ == "__main__":
    data_path = "./data/baseball_hitter"  # LabelMe JSON 파일이 있는 경로
    output_json = 'labelme2coco.json'     # 변환된 COCO JSON 파일 저장 경로
    labelme_to_coco(data_path, output_json)
