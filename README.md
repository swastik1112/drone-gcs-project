Clone the repository:
git clone https://github.com/swastik1112/drone-gcs-project.git
cd drone-gcs-project

Install dependencies:
pip install -r requirements.txt
Flask==2.0.1
flask-cors==3.1.1
pymavlink==2.4.3

Run the application:
python app.py

Run MAVProxy or connect to a drone:
mavproxy.py --master=udp:127.0.0.1:14550

Open the frontend:
Open index.html in your browser.
