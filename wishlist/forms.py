from django import forms

from wishlist.models import BarangWishlist

class WishlistForm(forms.ModelForm):
    class Meta:
        model = BarangWishlist
        fields = [
            'nama_barang',
            'harga_barang',
            'deskripsi',
        ]