import tkinter as tk
from tkinter import messagebox, Scrollbar, Listbox, Text, Entry, Button, Menu
from datetime import datetime

class CatatanHarianApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Catatan Harian Ilyas Ramadhan")

        # Struktur data yang digunakan untuk menyimpan catatan
        self.catatan = {}

        # Membuat menu
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Keluar", command=self.root.quit)
        help_menu = Menu(self.menu)
        self.menu.add_cascade(label="Bantuan", menu=help_menu)
        help_menu.add_command(label="Tentang", command=self.tentang)

        # Menggunakan widget untuk menginput judul
        self.judul_entry = Entry(self.root, width=50)
        self.judul_entry.grid(row=0, column=0, padx=10, pady=10)

        # Menggunakan widget untuk menginput isi catatan
        self.isi_text = Text(self.root, width=50, height=10, state='normal')
        self.isi_text.grid(row=1, column=0, padx=10, pady=10)

        # Tombol untuk menambah dan menghapus catatan
        self.tambah_button = Button(self.root, text="Tambah Catatan", command=self.tambah_catatan)
        self.tambah_button.grid(row=2, column=0, padx=10, pady=5)

        self.hapus_button = Button(self.root, text="Hapus Catatan", command=self.hapus_catatan)
        self.hapus_button.grid(row=3, column=0, padx=10, pady=5)

        # Listbox yang digunakan untuk menampilkan daftar catatan
        self.listbox = Listbox(self.root, width=50)
        self.listbox.grid(row=4, column=0, padx=10, pady=10)
        self.listbox.bind('<<ListboxSelect>>', self.tampilkan_catatan)

        # Scrollbar yang digunakan untuk listbox
        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.grid(row=4, column=1, sticky='ns')
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

    def tambah_catatan(self):
        judul = self.judul_entry.get().strip()
        isi = self.isi_text.get("1.0", tk.END).strip()

        if not judul or not isi:
            messagebox.showerror("Error", "Judul dan isi catatan harian tidak boleh kosong!")
            return

        # Menyimpan catatan dengan menggunakan timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.catatan[judul] = (isi, timestamp)
        self.listbox.insert(tk.END, f"{judul} ({timestamp})")
        self.judul_entry.delete(0, tk.END)
        self.isi_text.delete("1.0", tk.END)

    def tampilkan_catatan(self, event):
        try:
            selected_index = self.listbox.curselection()[0]
            selected_judul = self.listbox.get(selected_index).split(" (")[0]
            isi, _ = self.catatan[selected_judul]
            self.isi_text.config(state='normal')
            self.isi_text.delete("1.0", tk.END)
            self.isi_text.insert(tk.END, isi)
            self.isi_text.config(state='disabled')
        except IndexError:
            pass

    def hapus_catatan(self):
        try:
            selected_index = self.listbox.curselection()[0]
            selected_judul = self.listbox.get(selected_index).split(" (")[0]
            if messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus catatan harian '{selected_judul}'?"):
                del self.catatan[selected_judul]
                self.listbox.delete(selected_index)
                self.isi_text.config(state='normal')
                self.isi_text.delete("1.0", tk.END)
                self.isi_text.config(state='disabled')
        except IndexError:
            messagebox.showerror("Error", "Silakan pilih catatan harian yang ingin dihapus.")

    def tentang(self):
        messagebox.showinfo("Tentang", "Aplikasi catatan harian mulmull\nVersi 4.0")

if __name__ == "__main__":
    root = tk.Tk()
    app = CatatanHarianApp(root)
    root.mainloop()