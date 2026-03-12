import streamlit as st
import yt_dlp
import os

# Настройка страницы
st.set_page_config(page_title="CosmoDownloader", page_icon="💄")
st.title("💄 CosmoDownloader")
st.subheader("Загрузчик Shorts для твоего канала")

# Поле для ввода
url = st.text_input("Вставь ссылку на видео или Shorts здесь:", placeholder="https://youtube.com/shorts/...")

if url:
    try:
        with st.spinner('Анализирую видео...'):
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                thumbnail = info.get('thumbnail')

            st.image(thumbnail, width=300)
            st.write(f"**Название:** {title}")

            # Кнопка скачивания
            if st.button("Подготовить файл"):
                with st.spinner('Загрузка на сервер...'):
                    file_path = f"{title}.mp4"
                    ydl_opts_dl = {
                        'format': 'bestvideo+bestaudio/best',
                        'outtmpl': file_path,
                        'merge_output_format': 'mp4',
                    }
                    with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
                        ydl.download([url])
                    
                    # Читаем файл и отдаем пользователю
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="💾 Скачать на компьютер",
                            data=f,
                            file_name=f"{title}.mp4",
                            mime="video/mp4"
                        )
                    os.remove(file_path) # Удаляем с сервера после выдачи

    except Exception as e:
        st.error(f"Ошибка: {e}")