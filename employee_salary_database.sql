-- ============================================================
-- BANCO DE DADOS: GESTÃO DE SALÁRIOS E METAS DE FUNCIONÁRIOS
-- ============================================================

-- Remove tabelas existentes (ordem inversa por dependências)
DROP TABLE IF EXISTS bonus_pagamentos;
DROP TABLE IF EXISTS metas_progresso;
DROP TABLE IF EXISTS metas;
DROP TABLE IF EXISTS descontos;
DROP TABLE IF EXISTS folha_pagamento;
DROP TABLE IF EXISTS funcionarios;
DROP TABLE IF EXISTS cargos;
DROP TABLE IF EXISTS departamentos;

-- ============================================================
-- 1. DEPARTAMENTOS
-- ============================================================
CREATE TABLE departamentos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO departamentos (nome, descricao) VALUES
('Tecnologia', 'Desenvolvimento de software e infraestrutura'),
('Vendas', 'Equipe comercial e prospecção de clientes'),
('Recursos Humanos', 'Gestão de pessoas e recrutamento'),
('Financeiro', 'Contabilidade, tesouraria e planejamento financeiro'),
('Marketing', 'Comunicação, branding e campanhas');

-- ============================================================
-- 2. CARGOS
-- ============================================================
CREATE TABLE cargos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(100) NOT NULL,
    nivel ENUM('Junior', 'Pleno', 'Senior', 'Lider', 'Gerente', 'Diretor') NOT NULL,
    salario_base DECIMAL(10,2) NOT NULL,
    departamento_id INT NOT NULL,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
);

INSERT INTO cargos (titulo, nivel, salario_base, departamento_id) VALUES
('Desenvolvedor Backend', 'Junior', 3500.00, 1),
('Desenvolvedor Backend', 'Pleno', 6500.00, 1),
('Desenvolvedor Backend', 'Senior', 11000.00, 1),
('Desenvolvedor Frontend', 'Pleno', 6000.00, 1),
('Tech Lead', 'Lider', 14000.00, 1),
('Vendedor', 'Junior', 2500.00, 2),
('Vendedor', 'Pleno', 4000.00, 2),
('Gerente de Vendas', 'Gerente', 12000.00, 2),
('Analista de RH', 'Pleno', 5000.00, 3),
('Gerente de RH', 'Gerente', 10000.00, 3),
('Analista Financeiro', 'Pleno', 5500.00, 4),
('Controller', 'Senior', 9500.00, 4),
('Analista de Marketing', 'Pleno', 5000.00, 5),
('Gerente de Marketing', 'Gerente', 11000.00, 5);

-- ============================================================
-- 3. FUNCIONÁRIOS
-- ============================================================
CREATE TABLE funcionarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    data_nascimento DATE NOT NULL,
    data_admissao DATE NOT NULL,
    data_demissao DATE DEFAULT NULL,
    cargo_id INT NOT NULL,
    status ENUM('Ativo', 'Ferias', 'Afastado', 'Demitido') DEFAULT 'Ativo',
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cargo_id) REFERENCES cargos(id)
);

INSERT INTO funcionarios (nome, cpf, email, telefone, data_nascimento, data_admissao, cargo_id, status) VALUES
('Ana Silva', '111.222.333-44', 'ana.silva@empresa.com', '(11) 99999-0001', '1990-03-15', '2022-01-10', 3, 'Ativo'),
('Bruno Oliveira', '222.333.444-55', 'bruno.oliveira@empresa.com', '(11) 99999-0002', '1995-07-22', '2023-03-01', 2, 'Ativo'),
('Carla Santos', '333.444.555-66', 'carla.santos@empresa.com', '(11) 99999-0003', '1988-11-05', '2021-06-15', 5, 'Ativo'),
('Daniel Costa', '444.555.666-77', 'daniel.costa@empresa.com', '(11) 99999-0004', '1992-01-30', '2023-08-20', 1, 'Ativo'),
('Elena Ferreira', '555.666.777-88', 'elena.ferreira@empresa.com', '(11) 99999-0005', '1985-09-12', '2020-02-03', 8, 'Ativo'),
('Felipe Rocha', '666.777.888-99', 'felipe.rocha@empresa.com', '(11) 99999-0006', '1993-04-18', '2022-11-01', 7, 'Ativo'),
('Gabriela Lima', '777.888.999-00', 'gabriela.lima@empresa.com', '(11) 99999-0007', '1991-12-25', '2021-09-10', 9, 'Ativo'),
('Henrique Alves', '888.999.000-11', 'henrique.alves@empresa.com', '(11) 99999-0008', '1987-06-08', '2019-04-22', 10, 'Ativo'),
('Isabela Nunes', '999.000.111-22', 'isabela.nunes@empresa.com', '(11) 99999-0009', '1994-02-14', '2023-01-15', 11, 'Ativo'),
('João Mendes', '000.111.222-33', 'joao.mendes@empresa.com', '(11) 99999-0010', '1989-08-20', '2020-07-01', 12, 'Ativo'),
('Larissa Pereira', '111.333.555-77', 'larissa.pereira@empresa.com', '(11) 99999-0011', '1996-05-10', '2024-02-01', 4, 'Ativo'),
('Marcos Souza', '222.444.666-88', 'marcos.souza@empresa.com', '(11) 99999-0012', '1990-10-03', '2022-05-16', 6, 'Ativo'),
('Natalia Ribeiro', '333.555.777-99', 'natalia.ribeiro@empresa.com', '(11) 99999-0013', '1993-07-28', '2023-04-10', 13, 'Ativo'),
('Pedro Carvalho', '444.666.888-00', 'pedro.carvalho@empresa.com', '(11) 99999-0014', '1986-03-19', '2018-11-05', 14, 'Ativo'),
('Renata Dias', '555.777.999-11', 'renata.dias@empresa.com', '(11) 99999-0015', '1997-01-07', '2024-06-01', 1, 'Ativo');

-- ============================================================
-- 4. FOLHA DE PAGAMENTO (mensal)
-- ============================================================
CREATE TABLE folha_pagamento (
    id INT PRIMARY KEY AUTO_INCREMENT,
    funcionario_id INT NOT NULL,
    mes_referencia DATE NOT NULL COMMENT 'Primeiro dia do mês de referência',
    salario_bruto DECIMAL(10,2) NOT NULL,
    total_descontos DECIMAL(10,2) DEFAULT 0.00,
    total_bonus DECIMAL(10,2) DEFAULT 0.00,
    salario_liquido DECIMAL(10,2) GENERATED ALWAYS AS (salario_bruto - total_descontos + total_bonus) STORED,
    data_pagamento DATE,
    status ENUM('Pendente', 'Processado', 'Pago') DEFAULT 'Pendente',
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id),
    UNIQUE KEY uk_func_mes (funcionario_id, mes_referencia)
);

-- Folha de Jan/2026
INSERT INTO folha_pagamento (funcionario_id, mes_referencia, salario_bruto, total_descontos, total_bonus, data_pagamento, status) VALUES
(1, '2026-01-01', 11000.00, 2585.00, 0.00, '2026-01-30', 'Pago'),
(2, '2026-01-01', 6500.00, 1365.00, 0.00, '2026-01-30', 'Pago'),
(3, '2026-01-01', 14000.00, 3570.00, 0.00, '2026-01-30', 'Pago'),
(4, '2026-01-01', 3500.00, 630.00, 0.00, '2026-01-30', 'Pago'),
(5, '2026-01-01', 12000.00, 2940.00, 1200.00, '2026-01-30', 'Pago'),
(6, '2026-01-01', 4000.00, 760.00, 800.00, '2026-01-30', 'Pago'),
(7, '2026-01-01', 5000.00, 975.00, 0.00, '2026-01-30', 'Pago'),
(8, '2026-01-01', 10000.00, 2350.00, 0.00, '2026-01-30', 'Pago'),
(9, '2026-01-01', 5500.00, 1082.50, 0.00, '2026-01-30', 'Pago'),
(10, '2026-01-01', 9500.00, 2215.00, 0.00, '2026-01-30', 'Pago');

-- Folha de Fev/2026
INSERT INTO folha_pagamento (funcionario_id, mes_referencia, salario_bruto, total_descontos, total_bonus, data_pagamento, status) VALUES
(1, '2026-02-01', 11000.00, 2585.00, 1650.00, '2026-02-27', 'Pago'),
(2, '2026-02-01', 6500.00, 1365.00, 500.00, '2026-02-27', 'Pago'),
(3, '2026-02-01', 14000.00, 3570.00, 2100.00, '2026-02-27', 'Pago'),
(4, '2026-02-01', 3500.00, 630.00, 0.00, '2026-02-27', 'Pago'),
(5, '2026-02-01', 12000.00, 2940.00, 2400.00, '2026-02-27', 'Pago'),
(6, '2026-02-01', 4000.00, 760.00, 600.00, '2026-02-27', 'Pago'),
(7, '2026-02-01', 5000.00, 975.00, 0.00, '2026-02-27', 'Pago'),
(8, '2026-02-01', 10000.00, 2350.00, 500.00, '2026-02-27', 'Pago'),
(9, '2026-02-01', 5500.00, 1082.50, 0.00, '2026-02-27', 'Pago'),
(10, '2026-02-01', 9500.00, 2215.00, 0.00, '2026-02-27', 'Pago');

-- Folha de Mar/2026 (pendente)
INSERT INTO folha_pagamento (funcionario_id, mes_referencia, salario_bruto, total_descontos, total_bonus, status) VALUES
(1, '2026-03-01', 11000.00, 2585.00, 0.00, 'Processado'),
(2, '2026-03-01', 6500.00, 1365.00, 0.00, 'Processado'),
(3, '2026-03-01', 14000.00, 3570.00, 0.00, 'Processado'),
(4, '2026-03-01', 3500.00, 630.00, 0.00, 'Processado'),
(5, '2026-03-01', 12000.00, 2940.00, 0.00, 'Pendente');

-- ============================================================
-- 5. DESCONTOS (detalhamento por tipo)
-- ============================================================
CREATE TABLE descontos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    folha_id INT NOT NULL,
    tipo ENUM('INSS', 'IRRF', 'Vale_Transporte', 'Vale_Refeicao', 'Plano_Saude', 'Faltas', 'Adiantamento', 'Outros') NOT NULL,
    descricao VARCHAR(200),
    valor DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (folha_id) REFERENCES folha_pagamento(id)
);

-- Descontos de Ana Silva - Jan/2026 (folha_id=1)
INSERT INTO descontos (folha_id, tipo, descricao, valor) VALUES
(1, 'INSS', 'Contribuição previdenciária', 1210.00),
(1, 'IRRF', 'Imposto de renda retido na fonte', 825.00),
(1, 'Plano_Saude', 'Plano de saúde Unimed', 350.00),
(1, 'Vale_Refeicao', 'Desconto VR (parte funcionário)', 200.00);

-- Descontos de Bruno Oliveira - Jan/2026 (folha_id=2)
INSERT INTO descontos (folha_id, tipo, descricao, valor) VALUES
(2, 'INSS', 'Contribuição previdenciária', 715.00),
(2, 'IRRF', 'Imposto de renda retido na fonte', 350.00),
(2, 'Vale_Transporte', 'Desconto VT (6%)', 100.00),
(2, 'Vale_Refeicao', 'Desconto VR (parte funcionário)', 200.00);

-- Descontos de Carla Santos - Jan/2026 (folha_id=3)
INSERT INTO descontos (folha_id, tipo, descricao, valor) VALUES
(3, 'INSS', 'Contribuição previdenciária', 1540.00),
(3, 'IRRF', 'Imposto de renda retido na fonte', 1430.00),
(3, 'Plano_Saude', 'Plano de saúde Unimed Familiar', 600.00);

-- Descontos de Daniel Costa - Jan/2026 (folha_id=4)
INSERT INTO descontos (folha_id, tipo, descricao, valor) VALUES
(4, 'INSS', 'Contribuição previdenciária', 280.00),
(4, 'Vale_Transporte', 'Desconto VT (6%)', 150.00),
(4, 'Vale_Refeicao', 'Desconto VR (parte funcionário)', 200.00);

-- Descontos de Elena Ferreira - Jan/2026 (folha_id=5)
INSERT INTO descontos (folha_id, tipo, descricao, valor) VALUES
(5, 'INSS', 'Contribuição previdenciária', 1320.00),
(5, 'IRRF', 'Imposto de renda retido na fonte', 1020.00),
(5, 'Plano_Saude', 'Plano de saúde Unimed Familiar', 600.00);

-- ============================================================
-- 6. METAS
-- ============================================================
CREATE TABLE metas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT,
    departamento_id INT,
    funcionario_id INT,
    tipo ENUM('Individual', 'Equipe', 'Departamento') NOT NULL,
    metrica VARCHAR(100) NOT NULL COMMENT 'Ex: receita_vendas, tickets_resolvidos, etc.',
    valor_alvo DECIMAL(15,2) NOT NULL COMMENT 'Valor numérico a atingir',
    unidade VARCHAR(30) NOT NULL COMMENT 'Ex: R$, unidades, %, tickets',
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    bonus_percentual DECIMAL(5,2) DEFAULT 0.00 COMMENT '% do salário como bônus ao atingir 100%',
    status ENUM('Ativa', 'Concluida', 'Cancelada') DEFAULT 'Ativa',
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
);

INSERT INTO metas (titulo, descricao, funcionario_id, departamento_id, tipo, metrica, valor_alvo, unidade, data_inicio, data_fim, bonus_percentual, status) VALUES
-- Metas individuais de vendas
('Receita de vendas Q1', 'Atingir R$ 150.000 em vendas no primeiro trimestre', 5, 2, 'Individual', 'receita_vendas', 150000.00, 'R$', '2026-01-01', '2026-03-31', 20.00, 'Ativa'),
('Receita de vendas Q1', 'Atingir R$ 80.000 em vendas no primeiro trimestre', 6, 2, 'Individual', 'receita_vendas', 80000.00, 'R$', '2026-01-01', '2026-03-31', 15.00, 'Ativa'),
('Novos clientes Q1', 'Captar 20 novos clientes no trimestre', 12, 2, 'Individual', 'novos_clientes', 20.00, 'clientes', '2026-01-01', '2026-03-31', 10.00, 'Ativa'),

-- Metas de tecnologia
('Entregas de sprints', 'Completar 90% dos story points planejados', 1, 1, 'Individual', 'sprint_completion', 90.00, '%', '2026-01-01', '2026-03-31', 15.00, 'Ativa'),
('Redução de bugs', 'Reduzir bugs em produção em 30%', NULL, 1, 'Departamento', 'reducao_bugs', 30.00, '%', '2026-01-01', '2026-06-30', 10.00, 'Ativa'),
('Deploy contínuo', 'Implementar CI/CD completo para todos os projetos', 3, 1, 'Individual', 'projetos_cicd', 5.00, 'projetos', '2026-01-01', '2026-06-30', 20.00, 'Ativa'),

-- Metas de RH
('Redução de turnover', 'Reduzir taxa de turnover para menos de 5%', NULL, 3, 'Departamento', 'taxa_turnover', 5.00, '%', '2026-01-01', '2026-12-31', 10.00, 'Ativa'),
('Treinamentos realizados', 'Realizar 12 treinamentos internos no ano', 7, 3, 'Individual', 'treinamentos', 12.00, 'unidades', '2026-01-01', '2026-12-31', 10.00, 'Ativa'),

-- Metas de marketing
('Leads qualificados', 'Gerar 500 leads qualificados por mês', 13, 5, 'Individual', 'leads_mensais', 500.00, 'leads', '2026-01-01', '2026-03-31', 12.00, 'Ativa'),
('Engajamento redes sociais', 'Aumentar engajamento em 40%', NULL, 5, 'Departamento', 'engajamento_redes', 40.00, '%', '2026-01-01', '2026-06-30', 8.00, 'Ativa'),

-- Meta concluída (exemplo)
('Receita de vendas Q4/2025', 'Atingir R$ 120.000 em vendas no Q4', 5, 2, 'Individual', 'receita_vendas', 120000.00, 'R$', '2025-10-01', '2025-12-31', 20.00, 'Concluida');

-- ============================================================
-- 7. PROGRESSO DAS METAS
-- ============================================================
CREATE TABLE metas_progresso (
    id INT PRIMARY KEY AUTO_INCREMENT,
    meta_id INT NOT NULL,
    funcionario_id INT NOT NULL,
    data_registro DATE NOT NULL,
    valor_atual DECIMAL(15,2) NOT NULL,
    percentual_atingido DECIMAL(5,2) GENERATED ALWAYS AS (
        LEAST((valor_atual / (SELECT valor_alvo FROM metas WHERE metas.id = meta_id)) * 100, 100)
    ) STORED,
    observacao TEXT,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (meta_id) REFERENCES metas(id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
);

-- Progresso Meta 1: Elena - Receita vendas Q1 (alvo: R$ 150.000)
INSERT INTO metas_progresso (meta_id, funcionario_id, data_registro, valor_atual, observacao) VALUES
(1, 5, '2026-01-15', 18000.00, 'Primeiras semanas de prospecção'),
(1, 5, '2026-01-31', 52000.00, 'Fechamento de 3 contratos grandes'),
(1, 5, '2026-02-15', 78000.00, 'Pipeline aquecido'),
(1, 5, '2026-02-28', 110000.00, 'Excelente mês! Superou expectativa mensal'),
(1, 5, '2026-03-15', 138000.00, 'Próxima de bater a meta');

-- Progresso Meta 2: Felipe - Receita vendas Q1 (alvo: R$ 80.000)
INSERT INTO metas_progresso (meta_id, funcionario_id, data_registro, valor_atual, observacao) VALUES
(2, 6, '2026-01-31', 22000.00, 'Início promissor'),
(2, 6, '2026-02-28', 55000.00, 'Bom ritmo de vendas'),
(2, 6, '2026-03-15', 71000.00, 'Faltam R$ 9 mil para bater');

-- Progresso Meta 4: Ana - Sprint completion (alvo: 90%)
INSERT INTO metas_progresso (meta_id, funcionario_id, data_registro, valor_atual, observacao) VALUES
(4, 1, '2026-01-31', 85.00, 'Sprint 1 e 2 concluídas com boa taxa'),
(4, 1, '2026-02-28', 92.00, 'Melhorou no segundo mês'),
(4, 1, '2026-03-15', 91.00, 'Mantendo acima da meta');

-- Progresso Meta 6: Carla - CI/CD (alvo: 5 projetos)
INSERT INTO metas_progresso (meta_id, funcionario_id, data_registro, valor_atual, observacao) VALUES
(6, 3, '2026-01-31', 1.00, 'Projeto principal migrado'),
(6, 3, '2026-02-28', 3.00, 'Dois projetos adicionais configurados'),
(6, 3, '2026-03-15', 3.00, 'Sem avanço - aguardando aprovação de infra');

-- Progresso Meta 9: Natalia - Leads (alvo: 500/mês)
INSERT INTO metas_progresso (meta_id, funcionario_id, data_registro, valor_atual, observacao) VALUES
(9, 13, '2026-01-31', 420.00, 'Abaixo da meta, ajustando campanhas'),
(9, 13, '2026-02-28', 530.00, 'Superou a meta! Campanha do Carnaval deu certo'),
(9, 13, '2026-03-15', 310.00, 'Metade do mês, no ritmo');

-- ============================================================
-- 8. BÔNUS / PAGAMENTOS EXTRAS
-- ============================================================
CREATE TABLE bonus_pagamentos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    funcionario_id INT NOT NULL,
    folha_id INT,
    tipo ENUM('Meta_Atingida', 'Comissao', 'PLR', '13_Salario', 'Hora_Extra', 'Gratificacao', 'Indicacao') NOT NULL,
    descricao VARCHAR(300),
    valor DECIMAL(10,2) NOT NULL,
    meta_id INT DEFAULT NULL COMMENT 'Referência à meta quando aplicável',
    mes_referencia DATE NOT NULL,
    status ENUM('Aprovado', 'Pendente', 'Pago', 'Cancelado') DEFAULT 'Pendente',
    aprovado_por INT DEFAULT NULL,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id),
    FOREIGN KEY (folha_id) REFERENCES folha_pagamento(id),
    FOREIGN KEY (meta_id) REFERENCES metas(id),
    FOREIGN KEY (aprovado_por) REFERENCES funcionarios(id)
);

INSERT INTO bonus_pagamentos (funcionario_id, folha_id, tipo, descricao, valor, meta_id, mes_referencia, status, aprovado_por) VALUES
-- Janeiro
(5, 5, 'Comissao', 'Comissão sobre vendas de janeiro (2%)', 1200.00, 1, '2026-01-01', 'Pago', 8),
(6, 6, 'Comissao', 'Comissão sobre vendas de janeiro (2%)', 800.00, 2, '2026-01-01', 'Pago', 5),

-- Fevereiro
(1, 11, 'Meta_Atingida', 'Bônus por atingir meta de sprint (92%)', 1650.00, 4, '2026-02-01', 'Pago', 3),
(5, 15, 'Comissao', 'Comissão sobre vendas de fevereiro (2%)', 2400.00, 1, '2026-02-01', 'Pago', 8),
(6, 16, 'Comissao', 'Comissão sobre vendas de fevereiro (2%)', 600.00, 2, '2026-02-01', 'Pago', 5),
(3, 13, 'Meta_Atingida', 'Bônus parcial CI/CD - 3 de 5 projetos (60%)', 2100.00, 6, '2026-02-01', 'Pago', 8),
(2, 12, 'Hora_Extra', '12 horas extras em fevereiro', 500.00, NULL, '2026-02-01', 'Pago', 3),
(8, 18, 'Gratificacao', 'Gratificação por condução do processo seletivo', 500.00, NULL, '2026-02-01', 'Pago', 8),

-- Março (pendentes)
(5, NULL, 'Comissao', 'Comissão sobre vendas de março (estimativa)', 1800.00, 1, '2026-03-01', 'Pendente', NULL),
(13, NULL, 'Meta_Atingida', 'Bônus por superar meta de leads em fevereiro', 600.00, 9, '2026-03-01', 'Aprovado', 14),
(6, NULL, 'Comissao', 'Comissão sobre vendas de março (estimativa)', 500.00, 2, '2026-03-01', 'Pendente', NULL);

-- ============================================================
-- VIEWS ÚTEIS
-- ============================================================

-- View: Resumo da folha de pagamento com nome do funcionário
CREATE OR REPLACE VIEW vw_folha_resumo AS
SELECT
    fp.id AS folha_id,
    f.nome AS funcionario,
    c.titulo AS cargo,
    c.nivel,
    d.nome AS departamento,
    fp.mes_referencia,
    fp.salario_bruto,
    fp.total_descontos,
    fp.total_bonus,
    fp.salario_liquido,
    fp.status
FROM folha_pagamento fp
JOIN funcionarios f ON f.id = fp.funcionario_id
JOIN cargos c ON c.id = f.cargo_id
JOIN departamentos d ON d.id = c.departamento_id
ORDER BY fp.mes_referencia DESC, f.nome;

-- View: Progresso atual das metas ativas
CREATE OR REPLACE VIEW vw_metas_status AS
SELECT
    m.id AS meta_id,
    m.titulo,
    m.tipo,
    COALESCE(f.nome, CONCAT('Dept: ', d.nome)) AS responsavel,
    m.valor_alvo,
    m.unidade,
    COALESCE(mp.valor_atual, 0) AS ultimo_valor,
    ROUND(COALESCE(mp.valor_atual / m.valor_alvo * 100, 0), 1) AS percentual,
    m.bonus_percentual,
    m.data_fim,
    DATEDIFF(m.data_fim, CURDATE()) AS dias_restantes,
    m.status
FROM metas m
LEFT JOIN funcionarios f ON f.id = m.funcionario_id
LEFT JOIN departamentos d ON d.id = m.departamento_id
LEFT JOIN metas_progresso mp ON mp.meta_id = m.id
    AND mp.data_registro = (
        SELECT MAX(mp2.data_registro)
        FROM metas_progresso mp2
        WHERE mp2.meta_id = m.id
    )
WHERE m.status = 'Ativa'
ORDER BY percentual DESC;

-- View: Total de bônus por funcionário
CREATE OR REPLACE VIEW vw_bonus_total AS
SELECT
    f.nome AS funcionario,
    b.tipo,
    COUNT(*) AS quantidade,
    SUM(b.valor) AS total_bonus,
    MIN(b.mes_referencia) AS primeiro_bonus,
    MAX(b.mes_referencia) AS ultimo_bonus
FROM bonus_pagamentos b
JOIN funcionarios f ON f.id = b.funcionario_id
WHERE b.status IN ('Pago', 'Aprovado')
GROUP BY f.nome, b.tipo
ORDER BY total_bonus DESC;

-- ============================================================
-- CONSULTAS DE EXEMPLO
-- ============================================================

-- 1. Custo total da folha por departamento (mês atual)
SELECT
    d.nome AS departamento,
    COUNT(DISTINCT f.id) AS funcionarios,
    SUM(fp.salario_bruto) AS total_bruto,
    SUM(fp.total_descontos) AS total_descontos,
    SUM(fp.total_bonus) AS total_bonus,
    SUM(fp.salario_liquido) AS total_liquido
FROM folha_pagamento fp
JOIN funcionarios f ON f.id = fp.funcionario_id
JOIN cargos c ON c.id = f.cargo_id
JOIN departamentos d ON d.id = c.departamento_id
WHERE fp.mes_referencia = '2026-02-01'
GROUP BY d.nome
ORDER BY total_bruto DESC;

-- 2. Ranking de funcionários por bônus recebido no trimestre
SELECT
    f.nome,
    c.titulo AS cargo,
    SUM(b.valor) AS total_bonus_q1
FROM bonus_pagamentos b
JOIN funcionarios f ON f.id = b.funcionario_id
JOIN cargos c ON c.id = f.cargo_id
WHERE b.mes_referencia BETWEEN '2026-01-01' AND '2026-03-31'
  AND b.status IN ('Pago', 'Aprovado')
GROUP BY f.nome, c.titulo
ORDER BY total_bonus_q1 DESC;

-- 3. Metas próximas do prazo com menos de 80% atingido
SELECT
    m.titulo,
    COALESCE(f.nome, d.nome) AS responsavel,
    ROUND(COALESCE(mp.valor_atual / m.valor_alvo * 100, 0), 1) AS percentual,
    m.data_fim,
    DATEDIFF(m.data_fim, CURDATE()) AS dias_restantes
FROM metas m
LEFT JOIN funcionarios f ON f.id = m.funcionario_id
LEFT JOIN departamentos d ON d.id = m.departamento_id
LEFT JOIN metas_progresso mp ON mp.meta_id = m.id
    AND mp.data_registro = (
        SELECT MAX(mp2.data_registro) FROM metas_progresso mp2 WHERE mp2.meta_id = m.id
    )
WHERE m.status = 'Ativa'
  AND COALESCE(mp.valor_atual / m.valor_alvo * 100, 0) < 80
  AND DATEDIFF(m.data_fim, CURDATE()) <= 30
ORDER BY dias_restantes ASC;

-- 4. Evolução salarial (bruto + bônus) por funcionário nos últimos 3 meses
SELECT
    f.nome,
    fp.mes_referencia,
    fp.salario_bruto,
    fp.total_bonus,
    fp.salario_liquido
FROM folha_pagamento fp
JOIN funcionarios f ON f.id = fp.funcionario_id
WHERE f.id = 5  -- Elena Ferreira
ORDER BY fp.mes_referencia;
