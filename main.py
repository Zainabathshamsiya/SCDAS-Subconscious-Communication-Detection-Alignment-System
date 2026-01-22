from demos.demo_realtime import demo_realtime
from demos.demo_single_frame import demo_single_frame

print("SCDAS SYSTEM")
print("1. Real-time Demo")
print("2. Single Frame Demo")

choice = input("Enter choice: ")

if choice == '1':
    demo_realtime()
elif choice == '2':
    demo_single_frame()
