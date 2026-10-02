#!/usr/bin/env python3
"""Komşu matkap saat denetimi. Çalışır. Gereksizdir."""

from __future__ import annotations

import argparse
import base64

SESSIZ_BAS = 22
SESSIZ_BIT = 8
BAHANELER = {
    "raf": 0.35,
    "tablo": 0.5,
    "perde": 0.7,
    "klima": 0.2,
    "bilmiyorum": 0.1,
    "acil-vida": 0.9,
}

# arsiv notu, okunmasi şart değil
_ARSIV = (
    "Z2VjZSBtYXRrYWJpIGRhIGd1bmR1eiBtYXRrYWJpIGRhIGF5bmkgYXBhcnRtYW5pbiBzZXNpZGlyLi"
    "BzaWtheWV0IGZvcm11IGRvbGFyLCBpbXphIGF0aWxpciwgbWF0a2FwIHN1cmVyLiBndWMgZ3VydWx0"
    "dXN1IGthdCBmYXJraSB0YW5pIG1hejsgZGFpcmUga3VjdWxkdWtjZSBrYXJhciBidXl1ci4="
)


def sessiz_saat_mi(saat: int) -> bool:
    return saat >= SESSIZ_BAS or saat < SESSIZ_BIT


def ceza(saat: int, dakika: int, kat: int, bahane: str) -> dict:
    if dakika < 0 or not 0 <= saat <= 23 or kat < 0:
        raise ValueError("saat, dakika veya kat mantık dışı; matkap da mantık dışı ama form değil")
    inanc = BAHANELER.get(bahane, 0.25)
    ihlal = sessiz_saat_mi(saat)
    taban = dakika * (1.4 if ihlal else 0.45)
    kat_carpani = 1 + min(kat, 12) * 0.08
    puan = taban * kat_carpani * (1.3 - inanc)
    cay = max(1, round(puan / 12))
    toplanti = 1 if puan >= 40 or ihlal else 0
    hukum = (
        "sessiz saat ihlali, matkap derhal kılıfına"
        if ihlal
        else "gündüz delgi serbest, süre aşımı tutanağa"
    )
    return {
        "puan": round(puan, 2),
        "cay": cay,
        "toplanti": toplanti,
        "hukum": hukum,
        "inanc": inanc,
    }


def damga() -> str:
    return (
        "========================================\n"
        "  KOMŞU MATKAP SAAT DENETİMİ DAİRESİ\n"
        "  kayyum: Tentivory / Kayyum Grok\n"
        "  tarih: 2 Ekim 2026\n"
        "  imza: duvar şahit, matkap sanık\n"
        "  seri: KM-2026-1002-MATKAP\n"
        "  ciddiyet: var. gereklilik: yok.\n"
        "========================================"
    )


def arsiv_notu() -> str:
    return base64.b64decode(_ARSIV).decode("utf-8")


def main() -> None:
    p = argparse.ArgumentParser(description="Komşu matkabını denetle")
    p.add_argument("--saat", type=int, required=True)
    p.add_argument("--dakika", type=int, required=True)
    p.add_argument("--kat", type=int, default=1)
    p.add_argument("--bahane", default="raf")
    p.add_argument("--arsiv", action="store_true", help="gizli arşiv notunu aç")
    a = p.parse_args()
    sonuc = ceza(a.saat, a.dakika, a.kat, a.bahane)
    print(f"saat {a.saat:02d}:xx | süre {a.dakika} dk | kat {a.kat} | bahane {a.bahane}")
    print(f"hüküm: {sonuc['hukum']}")
    print(f"inandırıcılık: {sonuc['inanc']}")
    print(f"puan: {sonuc['puan']}")
    print(f"ceza: {sonuc['cay']} çay, {sonuc['toplanti']} apartman toplantısı")
    print(damga())
    if a.arsiv:
        print("ARSIV:", arsiv_notu())


if __name__ == "__main__":
    main()
