from flask import Flask, render_template, request, jsonify
import requests
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime

app = Flask(__name__)


API_KEY = 'acc_7662f0a8946e193'
API_SECRET = 'a4fd9dfd9b8e12dcc25bea247246483f'


SAMPLE_IMAGES = [
    {
        'id': 1,
        'url': 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=500',
        'title': 'Perro Golden Retriever'
    },
    {
        'id': 2,
        'url': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=500',
        'title': 'Gato Doméstico'
    },
    {
        'id': 3,
        'url': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=500',
        'title': 'Paisaje Urbano'
    },
   
    
]

def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='webapp_db',
        user='webapp_user',
        password='webapp_pass',
        port='5432'
    )
    return conn

def init_database():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS image_analysis (
                id SERIAL PRIMARY KEY,
                image_id INTEGER NOT NULL,
                image_url TEXT NOT NULL,
                image_title TEXT NOT NULL,
                tag1_name TEXT,
                tag1_confidence FLOAT,
                tag2_name TEXT,
                tag2_confidence FLOAT,
                analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                raw_response JSONB
            )
        ''')
        
        conn.commit()
        cur.close()
        conn.close()
        print("Base de datos inicializada correctamente")
    except Exception as e:
        print(f"Error inicializando base de datos: {e}")

@app.route('/')
def index():
    return render_template('index.html', images=SAMPLE_IMAGES)

@app.route('/analyze/<int:image_id>')
def analyze_image(image_id):
    # Buscar la imagen por ID
    image = next((img for img in SAMPLE_IMAGES if img['id'] == image_id), None)
    if not image:
        return jsonify({'error': 'Imagen no encontrada'}), 404
    
    try:
       
        response = requests.get(
            f'https://api.imagga.com/v2/tags?image_url={image["url"]}&language=en,es',
            auth=(API_KEY, API_SECRET)
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if 'result' in data and 'tags' in data['result']:
                tags = data['result']['tags']
                
             
                top_tags = sorted(tags, key=lambda x: x['confidence'], reverse=True)[:2]
                
                
                result = {
                    'image_id': image_id,
                    'image_url': image['url'],
                    'image_title': image['title'],
                    'tags': []
                }
                
                tag1_name = tag1_confidence = tag2_name = tag2_confidence = None
                
                for i, tag in enumerate(top_tags):
                    tag_info = {
                        'name_en': tag['tag']['en'],
                        'name_es': tag['tag'].get('es', tag['tag']['en']),
                        'confidence': round(tag['confidence'], 2)
                    }
                    result['tags'].append(tag_info)
                    
                    if i == 0:
                        tag1_name = tag['tag']['en']
                        tag1_confidence = tag['confidence']
                    elif i == 1:
                        tag2_name = tag['tag']['en']
                        tag2_confidence = tag['confidence']
                
                
                try:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    
                    cur.execute('''
                        INSERT INTO image_analysis 
                        (image_id, image_url, image_title, tag1_name, tag1_confidence, 
                         tag2_name, tag2_confidence, raw_response)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        image_id, image['url'], image['title'],
                        tag1_name, tag1_confidence, tag2_name, tag2_confidence,
                        json.dumps(data)
                    ))
                    
                    conn.commit()
                    cur.close()
                    conn.close()
                    
                    result['saved_to_db'] = True
                except Exception as db_error:
                    print(f"Error guardando en BD: {db_error}")
                    result['saved_to_db'] = False
                
                return jsonify(result)
            else:
                return jsonify({'error': 'No se encontraron tags en la respuesta'}), 500
        else:
            return jsonify({'error': f'Error de API: {response.status_code}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Error procesando imagen: {str(e)}'}), 500

@app.route('/history')
def history():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute('''
            SELECT * FROM image_analysis 
            ORDER BY analysis_date DESC 
            LIMIT 50
        ''')
        
        results = cur.fetchall()
        cur.close()
        conn.close()
        
        return render_template('history.html', results=results)
    except Exception as e:
        return f"Error accediendo al historial: {e}"

if __name__ == '__main__':
    init_database()
    app.run(host='0.0.0.0', port=5000, debug=True)