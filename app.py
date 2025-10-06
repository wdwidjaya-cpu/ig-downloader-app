from flask import Flask, request, jsonify
import instaloader
import os

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Inisialisasi Instaloader
L = instaloader.Instaloader()

# Membuat sebuah "endpoint" atau URL untuk diakses
# Contoh: http://domain-anda.com/download
@app.route('/download', methods=['POST'])
def download_media():
    # Mengambil data JSON yang dikirim ke endpoint ini
    data = request.get_json()
    
    # Memastikan ada 'url' di dalam data yang dikirim
    if not data or 'url' not in data:
        return jsonify({'error': 'URL tidak ditemukan di dalam request'}), 400

    URL = data['url']

    try:
        # Logika Instaloader yang sama seperti sebelumnya
        print(f"Menerima permintaan untuk URL: {URL}")
        shortcode = URL.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        target_folder = f"instagram_downloads_{post.owner_username}"

        # Mengunduh post ke folder di server hosting
        # Note: Di hosting, file ini mungkin akan terhapus setelah beberapa waktu (tergantung layanan)
        L.download_post(post, target=target_folder)
        
        print(f"Berhasil diunduh ke folder server: {target_folder}")

        # Mengirim respons sukses dalam format JSON
        return jsonify({
            'message': 'Download berhasil!',
            'owner': post.owner_username,
            'folder_di_server': target_folder
            # Di aplikasi nyata, Anda akan memberikan link langsung ke file,
            # bukan hanya nama folder di server.
        })

    except Exception as e:
        print(f"Terjadi error: {e}")
        # Mengirim respons error dalam format JSON
        return jsonify({'error': f'Gagal mengunduh. Pastikan link benar dan post publik. Detail: {str(e)}'}), 500

# Menjalankan aplikasi (hanya untuk tes di PC)
if __name__ == '__main__':
    app.run(debug=True)
