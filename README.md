# HKAGE - E2INO002C - Server

## A brief introduction of this program (for those who are interested in it)

> This programme series is designed to enhance students’ knowledge and interest in Artificial Intelligence (AI)
> and Internet of Things (IoT) through applying design thinking process to make smart living products.
> Students will engage in hands-on design challenges that focus on developing empathy, encouraging
> ideation, developing metacognitive awareness, and fostering creative problem-solving. Throughout the
> programme, students will acquire skills including computer-aided design (CAD) drawing, making a prototype
> by using 3D printer, laser cutter, electronic circuit, and computer programming. The group design mini
> project is targeted to inspire students in creativity, collaboration, and design talent.

– Quoted from [this PDF file](https://hkage.org.hk/flyer/5024_E2INO002C_en.pdf)

This code is written by Andy Zhang, participating in this program from Jan to Feb 2024 in Group 1.

Our project is a smart Newton's Cradle that tries to help those struggling with anxiety.

## What is this?

This is the server that runs on the smart device. It exchanges signals with the client
with [Socket.io](https://socket.io). The program consists of 2 files, each of them needs to be run separately.

### `recognition.py`

This script performs recognition, as the name suggests. It reads from `running.stat` to determine the running mode (Face
or Barcode).

The face recognition will try to derive a score based on the movement of the face. The algorithm is:

```Python
score = 0.5 / (np.std(key_points_dy_dx_mean) * 10) + 25
```

The barcode recognition will scan the webcam input for barcodes and append them to `barcodes.stat`, if they have never
been recognized before.

### `server.py`

This script performs client-server communication with [Socket.io](https://socket.io). This file handles a number of
signals, mainly:

- `start_face`, `start_face`

  Starts / Stops the face detection when the music plays / stops.

- `get_plans`

  Gets a list of the plans to be displayed in the "Plan" dialog in the client

- `save_plans`

  Saves the plans configured in the "Plan" dialog

- `start_barcode`, `stop_barcode`

  Starts / Stops the barcode detection.

## Get Started

To run this part of the project, you will need to:

1. Install [Python](https://python.org)
2. Install pip (if your Python installer did not add a `pip` command)
3. Clone the repository
   In the terminal window (if you are running macOS or Linux) or the Command Prompt (if you are running Windows), type:
   ```shell
   git clone https://github.com/ZCG-coder/e2ino002c-server.git
   ```
4. Install dependencies
   In the terminal window (if you are running macOS or Linux) or the Command Prompt (if you are running Windows), type:
   ```shell
   python3 -m pip install -r requirements.txt
   ```
5. Run the server
   In the terminal window (if you are running macOS or Linux) or the Command Prompt (if you are running Windows), type:
   ```shell
   python3 server.py
   ```
6. Run the recognition script
   In the terminal window (if you are running macOS or Linux) or the Command Prompt (if you are running Windows), type:
   ```shell
   python3 recognition.py
   ```
