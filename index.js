const express = require("express");
const cors = require("cors");
const pool = require("./pool");
require("dotenv").config();

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static("public"));

app.get("/", (req, res) => {
  res.send("API do Motoclube Tribo do Cerrado está online!");
});

app.post("/membros", async (req, res) => {
  const { nome, email, telefone } = req.body;
  try {
    const novo = await pool.query(
      "INSERT INTO membros (nome, email, telefone) VALUES ($1, $2, $3) RETURNING *",
      [nome, email, telefone]
    );
    res.json(novo.rows[0]);
  } catch (err) {
    console.error(err.message);
    res.status(500).send("Erro ao cadastrar membro");
  }
});

app.get("/membros", async (req, res) => {
  try {
    const todos = await pool.query("SELECT * FROM membros");
    res.json(todos.rows);
  } catch (err) {
    console.error(err.message);
    res.status(500).send("Erro ao listar membros");
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});