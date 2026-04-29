import express from 'express';
import path from 'path';

const app = express();
const PORT = 3000;

// This is a demo server for the AI Studio preview.
// The actual requested application logic is in app.py for your K8s environment.

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Mock database for preview
const meals = [
  { date: '2024-04-29', food_name: '샘플: 닭가슴살 샐러드', calories: 350, notes: '맛있음 (Preview Only)' }
];

app.get('/', (req, res) => {
  // We'll serve a static version of the template if we had one, 
  // but since we used Jinja templates in app.py, we'll just redirect to a simple info page 
  // or render a similar HTML here.
  res.send(`
    <html>
      <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>body { padding: 20px; font-family: sans-serif; }</style>
      </head>
      <body>
        <div class="alert alert-info">
          <h3>✅ Python Code Ready!</h3>
          <p>쿠버네티스 환경을 위한 <b>app.py, Dockerfile, requirements.txt</b> 파일이 생성이 완료되었습니다.</p>
          <hr>
          <p>현재 미리보기는 Node.js 데모 서버로 실행 중입니다. 실제 K8s 배포 시에는 생성된 Dockerfile을 사용하세요.</p>
        </div>
        <div class="card p-4">
          <h2>다이어트 식단 기록 (미리보기)</h2>
          <table class="table mt-4">
            <thead><tr><th>날짜</th><th>음식명</th><th>칼로리</th></tr></thead>
            <tbody>
              ${meals.map(m => `<tr><td>${m.date}</td><td>${m.food_name}</td><td>${m.calories}kcal</td></tr>`).join('')}
            </tbody>
          </table>
        </div>
      </body>
    </html>
  `);
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Demo Server running on port ${PORT}`);
});
