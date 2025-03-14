frm_Mon =   [   
                    0x00, 0x00,             # プロトコルID :0x0000
                    0x00, 0x06,             # 伝文長 :6 byte
                    0x00,                   # ユニットID :0
                    0x03,                   # FUNCTION CODE:0x03
                    0x01, 0x1C,             # レジスタアドレス:0x011C(リモートI/O R-OUT ~)
                    0x00, 0x1C              # 読み出し数 :28
                ] 
frm_ExeOpe =    [
                    0x00, 0x00,         # プロトコルID :0x0000
                    0x00, 0x2F,         # 伝文長 :47 byte
                    0x00,               # ユニットID :0
                    0x10,               # FUNCTION CODE:0x10
                    0x01, 0x04,         # レジスタアドレス:0x0104 (リモートI/O R-IN ~)
                    0x00, 0x14,         # 書き込みレジスタ数 :20
                    0x28,               # バイト数:40
                    0x00, 0x00,         # リモートI/O
                    0x00, 0x00,         # 運転データNoの選択
                    0x01, 0x00,         # 固定I/O (IN) TRIG ON
                    0x00, 0x01,         # ダイレクトデータ運転　運転方式                :2 相対位置決め（指令位置基準）#modified 0x02 to 0x01
                    #pos_2, pos_3,         # ダイレクトデータ運転　位置 (下位)             :8500 step  0x2134
                    0x27, 0x20,
                    #pos_0, pos_1,         # ダイレクトデータ運転　位置 (上位)
                    0x05, 0xDC,         # ダイレクトデータ運転　速度 (下位)             :2000 Hz
                    0x86,0xA0,
                    0x00, 0x01,         # ダイレクトデータ運転　速度 (上位)
                    0x07, 0xD0,         # ダイレクトデータ運転　起動・変速レート (下位)  :1.5 kHz/s
                    0x00, 0x00,         # ダイレクトデータ運転　起動・変速レート (上位)
                    0x05, 0xDC,         # ダイレクトデータ運転　停止レート (下位)       :1.5 kHz/s
                    0x00, 0x00,         # ダイレクトデータ運転　停止レート (上位)
                    0x03, 0xE8,         # ダイレクトデータ運転　運転電流                :100.0 %
                    0x00, 0x00,         # ダイレクトデータ運転　転送先
                    0x00, 0x00,         # 予約(reserved)
                    0x00, 0x00,         # リードパラメータID
                    0x00, 0x00,         # ライトリクエスト
                    0x00, 0x00,         # ライトパラメータID
                    0x00, 0x00,         # ライトデータ(下位)
                    0x00, 0x00          # ライトデータ(上位)
                ]

# ダイレクトデータ運転のトリガをOFFするクエリ
frm_ExeOpe_TrgOFF =        [
                        0x00, 0x00,         # プロトコルID :0x0000
                        0x00, 0x2F,         # 伝文長 :47 byte
                        0x00,               # ユニットID :0
                        0x10,               # FUNCTION CODE:0x10
                        0x01, 0x04,         # レジスタアドレス:0x0104 (リモートI/O R-IN ~)
                        0x00, 0x14,         # 書き込みレジスタ数 :20
                        0x28,               # バイト数:40
                        0x00, 0x00,         # リモートI/O
                        0x00, 0x00,         # 運転データNoの選択
                        0x00, 0x00,         # 固定I/O (IN) TRIG OFF
                        0x00, 0x01,         # ダイレクトデータ運転　運転方式                :2 相対位置決め（指令位置基準）
                        0x00, 0x00,         # ダイレクトデータ運転　位置 (下位)             :8500 step  0x2134
                        0x00, 0x00,         # ダイレクトデータ運転　位置 (上位)
                        0x05, 0xDC,         # ダイレクトデータ運転　速度 (下位)             :2000 Hz
                        0x00, 0x00,         # ダイレクトデータ運転　速度 (上位)
                        0x07, 0xD0,         # ダイレクトデータ運転　起動・変速レート (下位)  :1.5 kHz/s
                        0x00, 0x00,         # ダイレクトデータ運転　起動・変速レート (上位)
                        0x05, 0xDC,         # ダイレクトデータ運転　停止レート (下位)       :1.5 kHz/s
                        0x00, 0x00,         # ダイレクトデータ運転　停止レート (上位)
                        0x03, 0xE8,         # ダイレクトデータ運転　運転電流                :100.0 %
                        0x00, 0x00,         # ダイレクトデータ運転　転送先
                        0x00, 0x00,         # 予約(reserved)
                        0x00, 0x00,         # リードパラメータID
                        0x00, 0x00,         # ライトリクエスト
                        0x00, 0x00,         # ライトパラメータID
                        0x00, 0x00,         # ライトデータ(下位)
                        0x00, 0x00          # ライトデータ(上位)
                    ]