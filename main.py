from pathlib import Path
import yt_dlp

def ytdlp_to_mp3(urls, outdir="downloads", kbps=192):
    """
    urls: 文字列 or 文字列リスト（動画URL / プレイリストURL 混在OK）
    outdir: 出力ディレクトリ
    kbps: 128 / 192 / 320 など
    """
    Path(outdir).mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        # 最高音質の音声のみを取得
        "format": "bestaudio/best",
        # 出力ファイル名テンプレート
        "outtmpl": str(Path(outdir) / "%(title)s [%(id)s].%(ext)s"),
        # 取得後に FFmpeg で MP3 に変換（ビットレート指定）
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": str(kbps),  # '128' / '192' / '320'
            },
            # 可能ならメタデータも埋め込む
            {"key": "FFmpegMetadata"},
        ],
        # FFmpeg を優先して使う
        "prefer_ffmpeg": True,
        # 進捗表示（必要なければ True を False に）
        "noprogress": False,
        # 既存ファイルを上書きしたい場合は True
        "overwrites": False,
        # プレイリストURLなら全件取得（個々のURLでもそのまま動作）
        "yesplaylist": True,
        # YouTube 403エラー対策
        "cookiefile": None,  # Cookieファイルパスを指定可能
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"],
                "player_skip": ["configs"],
            }
        },
    }

    # 単一URLでも複数URLでも扱えるように
    if isinstance(urls, str):
        urls = [urls]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

if __name__ == "__main__":
    # 例：単体動画
    ytdlp_to_mp3("https://youtu.be/N9HV9gpq4f4?si=dBDa2Mg8bX55wRrp", kbps=192)
    # 例：プレイリスト
    # ytdlp_to_mp3("https://www.youtube.com/playlist?list=YYYYYYYYYYY", kbps=320)
