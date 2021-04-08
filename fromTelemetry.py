import irsdk
import pandas as pd
import matplotlib.pyplot as plt


def setup_dataframe(ir):
    throttle = ir.get_all('Throttle')
    brake = ir.get_all('Brake')
    session_time = ir.get_all('SessionTime')
    lap_dist_pct = ir.get_all('LapDistPct')
    player_car_in_pit_stall = ir.get_all('PlayerCarInPitStall')
    lap = ir.get_all('Lap')
    lap_completed = ir.get_all('LapCompleted')
    speed = ir.get_all('Speed')

    data = pd.DataFrame({
        'SessionTime': session_time,
        'LapDistPct': lap_dist_pct,
        'Speed': speed,
        'Throttle': throttle,
        'Brake': brake,
        'PlayerCarInPitStall': player_car_in_pit_stall,
        'Lap': lap,
        'LapCompleted': lap_completed
        })
    # print(data.head(5))
    return data


def split_stints(data: pd.DataFrame):
    stints = []
    stint = []
    for index, row in data.head(1000).iterrows():
        if row['PlayerCarInPitStall'] and row['Throttle'] == 0:
            if len(stint) > 0:
                stints.append(pd.DataFrame(stint))
            stint = []
            continue
        stint.append(row)

    if len(stint) > 0:
        stints.append(pd.DataFrame(stint))

    return stints


def split_stints_e(data: pd.DataFrame):
    data['c_id'] = (data.LapDistPct.diff() < 1e-9).cumsum()
    data['diff'] = data.LapDistPct.diff() < 1e-9
    for _, g in data.groupby((data.LapDistPct.diff() < 0.0).cumsum()):
        print(g)
    return data[data['PlayerCarInPitStall'] == True]


def plot(df: pd.DataFrame):
    plt.figure()
    df[['Throttle', 'Brake']].head(1000).plot(color={'Throttle': 'green', 'Brake': 'red'})
    plt.show()


if __name__ == '__main__':
    ir = irsdk.IBT()
    file_name = 'lamborghinievogt3_sebring international 2021-03-27 12-05-38'
    ir.open('data/telemetry/lamborghinievogt3_sebring international 2021-03-27 12-05-38.ibt')

    x = ir.get_all('SessionTime')

    data = setup_dataframe(ir)
    data.to_csv(f'data/{file_name}.csv', sep=';')
    # plot(data)
    stints = split_stints(data)
    s2 = split_stints_e(data)
    # s2.to_csv(f'data/test2.csv', sep=';')

    print('Done')
