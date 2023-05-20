from flask import Flask, request, render_template
import json
import xmltodict
import requests
from flask import jsonify



def on_json_loading_failed_return_dict(e):
	return {}

SECRET_KEY = '1234567890'  #Admin Key
url_getBusRouteList = 'http://apis.data.go.kr/6410000/busrouteservice/getBusRouteList'
url_getBusRouteStationList = 'http://apis.data.go.kr/6410000/busrouteservice/getBusRouteStationList'
url_getBusPredictTime = 'https://api.gbis.go.kr/ws/rest/busarrivalservice'


def Requests(url, params):
    response = requests.get(url, params=params)
    data_dict = xmltodict.parse(response.text)
    json_data = json.dumps(data_dict)
    result = json.loads(json_data)
    return result


def Correct_Bus(Bus_List, Correct_Bus_Number):
    try:
        result = Bus_List['response']['msgBody']['busRouteList']['routeId']
        return result
        
    except:
        LISTS=[]
        Feature_List=Bus_List['response']['msgBody']['busRouteList']
        for Feature in Feature_List:
          if Feature['routeName']==Correct_Bus_Number:
             LISTS.append([Feature['routeId'],[Feature['regionName'],Feature['routeTypeName']]])
        return jsonify(LISTS)


def Station_List(Bus_Route_Station_List):
    try:
        Bus_Route_Station_List_Important_Features = Bus_Route_Station_List[
            'response']['msgBody']['busRouteStationList']
        result = {
            Features['stationId']:
            {Features['stationName'], Features['turnYn']}
            for Features in Bus_Route_Station_List_Important_Features
        }
        return result
    except:
        print('Station_List 에서 오류')


def Predict_Bus_Time(Bus_And_Station):
    try:
        Predict_Time_one = Bus_And_Station['response']['msgBody'][
            'busArrivalItem']['predictTime1']
        Predict_Time_two = Bus_And_Station['response']['msgBody'][
            'busArrivalItem']['predictTime2']
        result = [Predict_Time_one, Predict_Time_two]
        if result[0] == None:
            result[0] = '차고지대기중'
        else:
            result[0] = result[0] + '분'
        if result[1] == None:
            result[1] = '차고지대기중'
        else:
            result[1] = result[1] + '분'

        return result
    except:
        print('Predict_Bus_Time 에서 오류')


app = Flask(__name__)


@app.route('/')
def start():

    return 'Hi'


@app.route('/GetBusList', methods=['POST'])
def process_post_request():
    Bus_Number = request.form['BUS_NUMBER']
    params ={'serviceKey': SECRET_KEY, 'keyword' : Bus_Number }
    Bus_List=Requests(url_getBusRouteList,params)
    Bus_RouteId=Correct_Bus(Bus_List,Bus_Number)
    print(type(Bus_RouteId))
    
    return Bus_RouteId


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
    # print('choice BUS number')#버스 번호입력
    # Buses=input()
    # params ={'serviceKey': SECRET_KEY, 'keyword' : Buses }
    # Bus_List=Requests(url_getBusRouteList,params)

    # Bus_RouteId=Correct_Bus(Bus_List,Buses)#특정버스 고르기

    # params ={'serviceKey' : SECRET_KEY, 'routeId' : Bus_RouteId }
    # Bus_Route_Station_List=Requests(url_getBusRouteStationList,params)
    # Station_List_Important_Features=Station_List(Bus_Route_Station_List)
    # print('choice station')
    # print(Station_List_Important_Features)
    # StationId=input()

    # params={
    # 'serviceKey': 1234567890,
    # 'stationId': StationId,
    # 'routeId': Bus_RouteId,
    # 'staOrder': 61
    # }

    # Two_Info=Requests(url_getBusPredictTime,params=params)
    # Predicted_Time=Predict_Bus_Time(Two_Info)
    # print("첫 번째 버스 도착시간:{}".format(Predicted_Time[0]))
    # print("두 번째 버스 도착시간:{}".format(Predicted_Time[1]))
