import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="CosmoDownloader", page_icon="💄")
st.title("💄 CosmoDownloader")
st.subheader("Загрузчик Shorts для твоего канала")

url = st.text_input("Вставь ссылку на видео или Shorts здесь:", placeholder="https://youtube.com/shorts/...")

if url:
    try:
        # Настройки для "маскировки" под браузер
        ydl_opts_base = {
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.google.com/',
        }

        with st.spinner('Анализирую видео...'):
            with yt_dlp.YoutubeDL(ydl_opts_base) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                thumbnail = info.get('thumbnail')

            st.image(thumbnail, width=300)
            st.write(f"**Название:** {title}")

            if st.button("Подготовить файл"):
                with st.spinner('Загрузка на сервер...'):
                    # Формируем имя файла без лишних символов
                    clean_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                    file_path = f"{clean_title}.mp4"
                    
                    ydl_opts_dl = {
                        **ydl_opts_base,
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        'outtmpl': file_path,
                        'merge_output_format': 'mp4',
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
                        ydl.download([url])
                    
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="💾 Скачать на компьютер",
                            data=f,
                            file_name=f"{clean_title}.mp4",
                            mime="video/mp4"
                        )
                    os.remove(file_path)

    except Exception as e:
        error_msg = str(e)
        if "403" in error_msg:
            st.error("YouTube временно ограничил доступ этому серверу. Попробуй обновить страницу или подождать 5 минут. Если не поможет — метод через Google Colab всегда работает стабильнее!")
        else:
            st.error(f"Ошибка: {e}")
