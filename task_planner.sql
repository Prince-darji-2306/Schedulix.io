-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 04, 2026 at 02:13 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `task_planner`
--

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `user_id`, `message`, `is_read`, `created_at`) VALUES
(1, 2, 'Plan approved and subtasks scheduled for task: 17', 1, '2026-02-24 16:26:24'),
(2, 2, 'Plan approved and subtasks scheduled for task: 17', 1, '2026-02-24 16:28:00'),
(3, 2, 'Plan approved and subtasks scheduled for task: 19', 1, '2026-02-24 17:23:43'),
(4, 2, 'Plan approved and subtasks scheduled for task: 20', 1, '2026-02-27 05:08:32'),
(5, 2, 'Plan approved and subtasks scheduled for task: 21', 1, '2026-02-27 08:24:32'),
(6, 2, 'Plan approved and subtasks scheduled for task: 28', 0, '2026-02-28 06:12:09'),
(7, 2, 'Plan approved and subtasks scheduled for task: 21', 0, '2026-02-28 06:29:53'),
(8, 2, 'Plan approved and subtasks scheduled for task: 30', 0, '2026-02-28 10:51:18'),
(9, 2, 'Plan approved and subtasks scheduled for task: 31', 0, '2026-02-28 10:59:32');

-- --------------------------------------------------------

--
-- Table structure for table `subtasks`
--

CREATE TABLE `subtasks` (
  `id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  `subtask` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `is_completed` tinyint(1) DEFAULT 0,
  `time_to` time NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `subtasks`
--

INSERT INTO `subtasks` (`id`, `task_id`, `subtask`, `description`, `is_completed`, `time_to`, `created_at`) VALUES
(40, 30, 'Theory & Demo', 'Study core concepts of Linear Regression, Decision Tree, and K‑Nearest Neighbors; watch 5‑min YouTube demos for each; run scikit‑learn Iris demos to see the algorithms in action.', 0, '00:00:00', '2026-02-28 10:51:18'),
(41, 30, 'Advanced Theory & Scratch', 'Read concise chapters on Random Forest and SVM; implement both algorithms from scratch using only NumPy; test on small arrays to ensure correctness.', 0, '00:00:00', '2026-02-28 10:51:18'),
(42, 30, 'Evaluation on Wine', 'Load the Wine dataset; train the two advanced models; compute accuracy, precision, recall; document the results for comparison.', 0, '00:00:00', '2026-02-28 10:51:18'),
(43, 30, 'Creative Build – CNN', 'Build a lightweight CNN with Keras to classify cat vs. dog images; use a small dataset; train quickly and evaluate performance.', 0, '00:00:00', '2026-02-28 10:51:18'),
(44, 30, 'Deployment', 'Create a Streamlit UI that loads the trained CNN; expose a local link for live demo; test the interface for usability.', 0, '00:00:00', '2026-02-28 10:51:18'),
(45, 30, 'Cheat‑Sheet & Wrap‑Up', 'Draft a concise one‑page cheat sheet summarizing key take‑aways, algorithm pros/cons, and hyper‑parameter insights; review all work and finalize.', 0, '00:00:00', '2026-02-28 10:51:18'),
(46, 31, 'Setup & Foundations', 'Install Anaconda/Miniconda, create a fresh Python 3.10 environment, install TensorFlow 2.15, PyTorch, JupyterLab, and essential libraries. Verify GPU availability. Watch a 1‑hour Deep Learning fundamentals video and quickly review linear algebra, calculus, and probability with flashcards.', 0, '17:24:00', '2026-02-28 10:59:32'),
(47, 31, 'Core Architecture & Mini‑Project', 'Build a 3‑layer MLP on MNIST, train, tweak learning rate, observe loss curves. Skim AlexNet, implement a tiny CNN on CIFAR‑10 with data augmentation, batch‑norm, and dropout. Compare validation accuracy.', 0, '18:19:00', '2026-02-28 10:59:32'),
(48, 31, 'Advanced Concepts & Hands‑On', 'Skim the Attention paper, implement a toy transformer encoder on a small text dataset, experiment briefly with an LSTM on the same data to contrast performance.', 0, '19:14:00', '2026-02-28 10:59:32'),
(49, 31, 'Visualization & Interactive Demo', 'Launch TensorBoard and use the Embedding Projector to animate MLP clustering on MNIST. Build a Streamlit app that lets you tweak weights in real time and observe predictions on a toy image. Record a short video of the demo.', 0, '20:09:00', '2026-02-28 10:59:32'),
(50, 31, 'Creative Exploration & Portfolio', 'Write a short story with a neuron character to explain activations. Convert a famous painting to pixel data, train a small CNN to classify its style, interpret filters as brush strokes. Create a “Deep‑Learning Quest” card game for quick concept quizzes.', 0, '21:04:00', '2026-02-28 10:59:32'),
(51, 31, 'Reflection & Next Steps', 'Evaluate all models: metrics, loss curves, TensorBoard summaries. Log results in a Markdown table, embed key plots, write a concise reflection. Draft a 2‑page PDF portfolio with code snippets and screenshots. Plan next week’s focus (RNNs, GANs, transfer learning) and commit to sharing the repo on GitHub.', 0, '22:00:00', '2026-02-28 10:59:32');

-- --------------------------------------------------------

--
-- Table structure for table `tasks`
--

CREATE TABLE `tasks` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `deadline_date` date DEFAULT NULL,
  `time` time(4) NOT NULL,
  `status` enum('pending','in_progress','completed','overdue') DEFAULT 'pending',
  `ai_plan_json` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`ai_plan_json`)),
  `plan_approved` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tasks`
--

INSERT INTO `tasks` (`id`, `user_id`, `title`, `description`, `deadline_date`, `time`, `status`, `ai_plan_json`, `plan_approved`) VALUES
(30, 2, 'Ml algorithms', 'Learn Ml algorithm Implementations', '2026-02-28', '18:00:00.0000', 'pending', '{\"final_plan\": \"{\\n  \\\"markdown_plan\\\": \\\"# Optimized ML Algorithms Plan (16:20\\u202f\\u2013\\u202f18:00)\\\\n\\\\n**Goal**: Deliver a concise, theory\\u2011rich, implementation\\u2011heavy, and creative demonstration of machine\\u2011learning algorithms within the 1\\u202fh\\u202f40\\u202fmin window.\\\\n\\\\n**Structure**:\\\\n1. **Quick Theory & Demo** \\u2013 Master the fundamentals of Linear Regression, Decision Tree, and K\\u2011Nearest Neighbors.\\\\n2. **Advanced Theory & Scratch Coding** \\u2013 Dive into Random Forest and SVM, implementing both from scratch.\\\\n3. **Hands\\u2011On Evaluation** \\u2013 Train and evaluate the two advanced models on the Wine dataset.\\\\n4. **Creative Build** \\u2013 Construct a lightweight CNN image classifier (cat vs. dog) using Keras.\\\\n5. **Deployment** \\u2013 Wrap the model in a Streamlit web app and publish a local demo link.\\\\n6. **Cheat\\u2011Sheet & Wrap\\u2011Up** \\u2013 Summarize key take\\u2011aways in a one\\u2011page cheat sheet.\\\\n\\\\nAll tasks are timed to fit exactly 100 minutes, ensuring a smooth flow from theory to deployment.\\\\n\\\\n---\\\\n\\\\n**Subtasks**\\\\n\\\\n| Time | Subtask | Description |\\\\n|------|---------|-------------|\\\\n| 16:20\\u201116:40 | **Theory & Demo** | Study core concepts of Linear Regression, Decision Tree, K\\u2011Nearest Neighbors; watch 5\\u2011min YouTube demos; run scikit\\u2011learn Iris demos. |\\\\n| 16:40\\u201117:05 | **Advanced Theory & Scratch** | Read concise chapters on Random Forest & SVM; implement each from scratch using NumPy; debug and validate logic. |\\\\n| 17:05\\u201117:20 | **Evaluation on Wine** | Load Wine dataset; train both models; compute accuracy, precision, recall; record results. |\\\\n| 17:20\\u201117:40 | **Creative Build \\u2013 CNN** | Build a simple CNN with Keras to classify cat vs. dog images; train on a small dataset; evaluate quickly. |\\\\n| 17:40\\u201117:50 | **Deployment** | Create a Streamlit UI; load the trained CNN; expose a local link for demo. |\\\\n| 17:50\\u201118:00 | **Cheat\\u2011Sheet & Wrap\\u2011Up** | Draft a concise cheat sheet summarizing algorithms, pros/cons, and key hyper\\u2011parameters; review plan. |\\\\n\\\\n---\\\\n\\\\n**Result**: By the 18:00 deadline, you\\u2019ll have a polished cheat sheet, a functioning image classifier, and a live Streamlit demo\\u2014all rooted in solid theoretical understanding and hands\\u2011on coding.\\\\n\\\",\\n  \\\"subtasks\\\": [\\n    {\\n      \\\"subtask\\\": \\\"Theory & Demo\\\",\\n      \\\"description\\\": \\\"Study core concepts of Linear Regression, Decision Tree, and K\\u2011Nearest Neighbors; watch 5\\u2011min YouTube demos for each; run scikit\\u2011learn Iris demos to see the algorithms in action.\\\",\\n      \\\"time_to\\\": \\\"16:20\\\"\\n    },\\n    {\\n      \\\"subtask\\\": \\\"Advanced Theory & Scratch\\\",\\n      \\\"description\\\": \\\"Read concise chapters on Random Forest and SVM; implement both algorithms from scratch using only NumPy; test on small arrays to ensure correctness.\\\",\\n      \\\"time_to\\\": \\\"16:40\\\"\\n    },\\n    {\\n      \\\"subtask\\\": \\\"Evaluation on Wine\\\",\\n      \\\"description\\\": \\\"Load the Wine dataset; train the two advanced models; compute accuracy, precision, recall; document the results for comparison.\\\",\\n      \\\"time_to\\\": \\\"17:05\\\"\\n    },\\n    {\\n      \\\"subtask\\\": \\\"Creative Build \\u2013 CNN\\\",\\n      \\\"description\\\": \\\"Build a lightweight CNN with Keras to classify cat vs. dog images; use a small dataset; train quickly and evaluate performance.\\\",\\n      \\\"time_to\\\": \\\"17:20\\\"\\n    },\\n    {\\n      \\\"subtask\\\": \\\"Deployment\\\",\\n      \\\"description\\\": \\\"Create a Streamlit UI that loads the trained CNN; expose a local link for live demo; test the interface for usability.\\\",\\n      \\\"time_to\\\": \\\"17:40\\\"\\n    },\\n    {\\n      \\\"subtask\\\": \\\"Cheat\\u2011Sheet & Wrap\\u2011Up\\\",\\n      \\\"description\\\": \\\"Draft a concise one\\u2011page cheat sheet summarizing key take\\u2011aways, algorithm pros/cons, and hyper\\u2011parameter insights; review all work and finalize.\\\",\\n      \\\"time_to\\\": \\\"17:50\\\"\\n    }\\n  ]\\n}\"}', 1),
(31, 2, 'Learn Deep learning', 'Want to Learn deep learning from scratch with full assumptions and everything.', '2026-02-28', '22:00:00.0000', 'in_progress', '{\"final_plan\": \"{\\n  \\\"markdown_plan\\\": \\\"# 5\\u202fh\\u202f30\\u202fmin Deep Learning Crash & Exploration Plan\\\\n\\\\n**Time window**: 16:29\\u202f\\u2013\\u202f22:00 (5\\u202fh\\u202f31\\u202fmin). 6 adaptive subtasks, each 55\\u201156\\u202fmin, cover everything from environment setup to creative exploration and reflection.\\\\n\\\\n## 1\\ufe0f\\u20e3 Setup & Foundations (55\\u202fmin) \\u2013 *Ends at 17:24*\\\\n- Install Anaconda (or Miniconda) and create a fresh env: `conda create -n dl_env python=3.10`. \\\\n- Activate it and install core libraries: `pip install tensorflow==2.15 torch torchvision matplotlib seaborn jupyterlab`. \\\\n- Spin up JupyterLab (`jupyter lab`) and verify GPU availability with `tf.config.list_physical_devices(\'GPU\')`. \\\\n- Watch the 1\\u2011h \\u201cDeep Learning Fundamentals\\u201d YouTube playlist (or equivalent). \\\\n- Quick review of linear algebra, calculus, and probability concepts with flashcards or an online quiz.\\\\n\\\\n## 2\\ufe0f\\u20e3 Core Architecture & Mini\\u2011Project (55\\u202fmin) \\u2013 *Ends at 18:19*\\\\n- Build a 3\\u2011layer MLP on MNIST: data loading, model definition, training loop, loss curve inspection. \\\\n- Tweak learning rate and optimizer; note the effect on convergence. \\\\n- Read the AlexNet paper (15\\u202fmin skim) and implement a tiny CNN on CIFAR\\u201110 (Conv\\u2011Pool\\u2011FC). \\\\n- Add data augmentation, batch\\u2011norm, and dropout; compare validation accuracy.\\\\n\\\\n## 3\\ufe0f\\u20e3 Advanced Concepts & Hands\\u2011On (55\\u202fmin) \\u2013 *Ends at 19:14*\\\\n- Skim \\u201cAttention is All You Need\\u201d (focus on scaled dot\\u2011product attention). \\\\n- Implement a toy transformer encoder on a small text dataset (e.g., character\\u2011level next\\u2011token prediction). \\\\n- Briefly experiment with an RNN (LSTM) on the same data to contrast performance.\\\\n\\\\n## 4\\ufe0f\\u20e3 Visualization & Interactive Demo (55\\u202fmin) \\u2013 *Ends at 20:09*\\\\n- Launch TensorBoard and use the Embedding Projector to animate how the MLP clusters MNIST digits. \\\\n- Build a Streamlit app that lets you adjust weights/activations in real time and see predictions on a toy image. \\\\n- Record a short video of the live demo for future reference.\\\\n\\\\n## 5\\ufe0f\\u20e3 Creative Exploration & Portfolio (55\\u202fmin) \\u2013 *Ends at 21:04*\\\\n- Write a short story where a \\u201cneuron\\u201d is a character to explain activation functions. \\\\n- Convert a famous painting to a pixel array and train a small CNN to classify its style; interpret learned filters as \\u201cbrush strokes.\\u201d \\\\n- Create a \\u201cDeep\\u2011Learning Quest\\u201d card game (concept cards + quick quiz) to test knowledge in a gamified way.\\\\n\\\\n## 6\\ufe0f\\u20e3 Reflection & Next Steps (56\\u202fmin) \\u2013 *Ends at 22:00*\\\\n- Evaluate all models: metrics, loss curves, and TensorBoard summaries. \\\\n- Log results in a Markdown table, embed key plots, and write a concise reflection. \\\\n- Draft a 2\\u2011page PDF portfolio (code snippets, screenshots, learning outcomes). \\\\n- Plan the next week\\u2019s focus (RNNs, GANs, transfer learning) and commit to sharing the repo on GitHub.\\\\n\\\\n**Total time**: 331\\u202fmin (5\\u202fh\\u202f31\\u202fmin) \\u2013 fits perfectly within the 16:29\\u202f\\u2013\\u202f22:00 window.\\\\n\\\\nEnjoy the journey from fundamentals to creativity! \\ud83d\\ude80\\\",\\n  \\\"subtasks\\\": [\\n    {\\n      \\\"subtask\\\": \\\"Setup & Foundations\\\",\\n      \\\"description\\\": \\\"Install Anaconda/Miniconda, create a fresh Python 3.10 environment, install TensorFlow 2.15, PyTorch, JupyterLab, and essential libraries. Verify GPU availability. Watch a 1\\u2011hour Deep Learning fundamentals video and quickly review linear algebra, calculus, and probability with flashcards.\\\",\\n      \\\"time_to\\\": \\\"17:24\\\"\\n    },\\n    {\\n      \\\"subtask\\\": \\\"Core Architecture & Mini\\u2011Project\\\",\\n      \\\"description\\\": \\\"Build a 3\\u2011layer MLP on MNIST, train, tweak learning rate, observe loss curves. Skim AlexNet, implement a tiny CNN on CIFAR\\u201110 with data augmentation, batch\\u2011norm, and dropout. Compare validation accuracy.\\\",\\n      \\\"time_to\\\": \\\"18:19\\\"\\n    },\\n    {\\n      \\\"subtask\\\": \\\"Advanced Concepts & Hands\\u2011On\\\",\\n      \\\"description\\\": \\\"Skim the Attention paper, implement a toy transformer encoder on a small text dataset, experiment briefly with an LSTM on the same data to contrast performance.\\\",\\n      \\\"time_to\\\": \\\"19:14\\\"\\n    },\\n    {\\n      \\\"subtask\\\": \\\"Visualization & Interactive Demo\\\",\\n      \\\"description\\\": \\\"Launch TensorBoard and use the Embedding Projector to animate MLP clustering on MNIST. Build a Streamlit app that lets you tweak weights in real time and observe predictions on a toy image. Record a short video of the demo.\\\",\\n      \\\"time_to\\\": \\\"20:09\\\"\\n    },\\n    {\\n      \\\"subtask\\\": \\\"Creative Exploration & Portfolio\\\",\\n      \\\"description\\\": \\\"Write a short story with a neuron character to explain activations. Convert a famous painting to pixel data, train a small CNN to classify its style, interpret filters as brush strokes. Create a \\u201cDeep\\u2011Learning Quest\\u201d card game for quick concept quizzes.\\\",\\n      \\\"time_to\\\": \\\"21:04\\\"\\n    },\\n    {\\n      \\\"subtask\\\": \\\"Reflection & Next Steps\\\",\\n      \\\"description\\\": \\\"Evaluate all models: metrics, loss curves, TensorBoard summaries. Log results in a Markdown table, embed key plots, write a concise reflection. Draft a 2\\u2011page PDF portfolio with code snippets and screenshots. Plan next week\\u2019s focus (RNNs, GANs, transfer learning) and commit to sharing the repo on GitHub.\\\",\\n      \\\"time_to\\\": \\\"22:00\\\"\\n    }\\n  ]\\n}\"}', 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password_hash`) VALUES
(2, 'john', 'john@gmail.com', '$2b$12$e8iShERTRopYk7CdMyHbMOtucpDXwK1C13C2iFzjSkOn18VWPGsVi');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `subtasks`
--
ALTER TABLE `subtasks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_task` (`task_id`);

--
-- Indexes for table `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `subtasks`
--
ALTER TABLE `subtasks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `subtasks`
--
ALTER TABLE `subtasks`
  ADD CONSTRAINT `fk_task` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `tasks`
--
ALTER TABLE `tasks`
  ADD CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
