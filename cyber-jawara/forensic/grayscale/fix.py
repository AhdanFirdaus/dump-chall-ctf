from PIL import Image, ImageSequence
import io

def repair_gif(input_path, output_path):
    try:
        # Buka file GIF menggunakan Pillow
        with Image.open(input_path) as im:
            # Pastikan file adalah GIF
            if im.format != 'GIF':
                raise ValueError("File bukan GIF")

            # Membaca semua frame dan menyimpan frame yang valid
            frames = []
            for frame in ImageSequence.Iterator(im):
                try:
                    frame.verify()  # Memverifikasi frame
                    frames.append(frame.copy())
                except Exception as e:
                    print(f"Frame rusak dilewati: {e}")

            if not frames:
                raise ValueError("Tidak ada frame yang valid")

            # Simpan GIF yang diperbaiki
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                loop=im.info.get('loop', 0),
                duration=im.info.get('duration', 100),
                optimize=True,
            )
            print(f"GIF berhasil diperbaiki dan disimpan di {output_path}")

    except Exception as e:
        print(f"Kesalahan saat memperbaiki GIF: {e}")

# Ganti 'damaged.gif' dengan path file GIF rusak Anda dan 'fixed.gif' sebagai output
repair_gif("g.gif", "fixed.gif")
