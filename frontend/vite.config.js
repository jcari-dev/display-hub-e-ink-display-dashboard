import react from "@vitejs/plugin-react-swc";
import { defineConfig } from "vite";

export default defineConfig({
	plugins: [react()],
	server: {
		proxy: {
			"/settings": {
				target: "http://pi400.local:8001", // Backend URL
				changeOrigin: true, // Makes the origin header match the target
				secure: false, // Allows self-signed certificates
			},
		},
	},
});
