import pandas as pd
import random
from datetime import datetime, timedelta

mac_addresses = [f"AA:BB:CC:DD:EE:{str(i).zfill(2)}" for i in range(4)]
statuses = ['online', 'online', 'offline', 'offline']
overview_active_hardware = pd.DataFrame({
    'MAC': mac_addresses,
    'Status': statuses
})

base_time = datetime.now()
traffic_data = {
    "traffic_num": [random.randint(90, 100) for _ in range(10)],
    "time": [(base_time + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(10)]
}
overview_traffic = pd.DataFrame(traffic_data)

nama_siswa = ['Asep Sunarta', 'Dina Fritz', 'Golden Batch', 'Stecu Shefirst', 'Filo Ackerman']
kelas_siswa = [7, 8, 7, 8, 9,]
kehadiran = [0.8, 0.8, 0.7, 0.5, 0.7]
data_mahasiswa = {
    'Nama': nama_siswa,
    'Kelas': kelas_siswa,
    'Persentase Kehadiran': kehadiran
}

mahasiswa_data = pd.DataFrame(data_mahasiswa)
