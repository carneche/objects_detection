FROM python:3.7
ADD . /app/
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt
EXPOSE 8501
CMD streamlit run objects_detection.py