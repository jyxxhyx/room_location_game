from model.room_location import RoomLocation
from output_handler.drawer import draw_solution


def main():
    m = 7
    n = 7
    k = 4
    model = RoomLocation(m,n,k)
    coords, flags = model.solve()
    draw_solution(f'data/output/{m}_{n}_{k}', (m, n), coords, flags)
    print(coords)
    print(flags)
    return


if __name__ == '__main__':
    main()
