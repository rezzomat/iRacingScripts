import irsdk
import pandas as pd
import matplotlib.pyplot as plt

ir = irsdk.IBT()
ir.open('data/bmwm4gt3_nurburgring combined 2021-03-30 17-43-06.ibt')

x = ir.get_all('SessionTime')


def setup_data(session_time, lap_dist_pct, throttle, brake, player_car_in_pit_stall):
    data = pd.DataFrame({
        'SessionTime': session_time,
        'LapDistPct': lap_dist_pct,
        'Throttle': throttle,
        'Brake': brake,
        'PlayerCarInPitStall': player_car_in_pit_stall
        })
    print(data.head(5))
    return data


def plot(df: pd.DataFrame):
    plt.figure()
    df[['Throttle', 'Brake']].head(1000).plot(color={'Throttle': 'green', 'Brake': 'red'})
    plt.show()


if __name__ == '__main__':
    print('hi')
    throttle = ir.get_all('Throttle')
    brake = ir.get_all('Brake')
    session_time = ir.get_all('SessionTime')
    lap_dist_pct = ir.get_all('LapDistPct')
    player_car_in_pit_stall = ir.get_all('PlayerCarInPitStall')

    data = setup_data(session_time, lap_dist_pct, throttle, brake, player_car_in_pit_stall)
    plot(data)

    print(len(throttle), len(session_time), len(lap_dist_pct))
