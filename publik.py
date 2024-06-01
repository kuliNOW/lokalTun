import sys
import ngrok
import requests
import asyncio
    
def config():
    authtoken = "isikan auth token anda"
    port = 80 
    proto = "http"
    return authtoken, port, proto

async def checker(target):
    print(f"\nCek ip mikrotik: {target}")
    token, port, proto = config()
    listener = await ngrok.forward(
        addr=f"{target}:{port}",
        authtoken=token, 
        proto=proto
        )
    publik = listener.url()
    return publik

async def connector(target):
    print(f"Merubah ip lokal agar bisa diakses publik")
    token, port, proto = config()
    publik = await ngrok.connect(
        addr=f"{target}:{port}",
        authtoken=token,
        proto=proto
        )
    print(f"Mikrotik sudah bisa diakses publik: {publik.url()}")
    await asyncio.Event().wait()

async def main(target):
    url =  None
    try:
        url = await checker(target)
        header = {
            'ngrok-skip-browser-warning': 'true'
        }
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            try:
                print("Ip Mikrotik bisa diakses")
                await connector(target)
            except KeyboardInterrupt:
                print("Tunnel dihentikan")
                ngrok.disconnect(url)
        else:
            print("Ip miktorik tidak dapat diakses\nSilahkan cek ulang ip mikrotik\n")
            ngrok.disconnect(url)
    except ValueError as e:
        print(e)
    except KeyboardInterrupt:
        if url:
            print("Tunnel dihentikan")
            ngrok.disconnect(url)
    except Exception as e:
        print(f"Terjadi kesalahan {e}")
        if url:
            print("Tunnel dihentikan")
            ngrok.disconnect(url)

if len(sys.argv) == 2:
    try:
        ip = sys.argv[1]
        asyncio.run(main(ip))
    except KeyboardInterrupt:
        print("Program dihentikan\n")
else:
    print("\nPenggunaan:\n  python.exe publik.py [ip mikrotik]\n")