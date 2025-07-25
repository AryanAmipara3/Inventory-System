-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 25, 2025 at 12:36 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inventory_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`) VALUES
(1, 'Grocery'),
(2, 'Personal Care'),
(3, 'Fashion'),
(4, 'Electronics'),
(5, 'Stationery');

-- --------------------------------------------------------

--
-- Table structure for table `goods_receiving`
--

CREATE TABLE `goods_receiving` (
  `id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `supplier_id` int(11) DEFAULT NULL,
  `quantity` float DEFAULT NULL,
  `unit` varchar(50) DEFAULT NULL,
  `rate` decimal(10,2) DEFAULT NULL,
  `total_rate` decimal(10,2) DEFAULT NULL,
  `tax` decimal(10,2) DEFAULT NULL,
  `received_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `goods_receiving`
--

INSERT INTO `goods_receiving` (`id`, `product_id`, `supplier_id`, `quantity`, `unit`, `rate`, `total_rate`, `tax`, `received_at`) VALUES
(1, 1, 1, 5, 'kg', 80.00, 400.00, 20.00, '2025-07-25 15:51:57'),
(2, 6, 3, 10, 'pcs', 850.00, 8500.00, 1530.00, '2025-07-25 15:52:18'),
(4, 10, 5, 100, 'pcs', 72.00, 7200.00, 864.00, '2025-07-25 15:57:56');

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `product_id` int(11) NOT NULL,
  `quantity` float DEFAULT 0,
  `min_stock` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`product_id`, `quantity`, `min_stock`) VALUES
(1, 1, 2),
(6, 2, 5),
(10, 80, 20);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `barcode` varchar(100) DEFAULT NULL,
  `sku_id` varchar(100) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `subcategory_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `gst_tax` float DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `default_unit` varchar(50) DEFAULT NULL,
  `conversion_factor` float DEFAULT NULL,
  `image_path` text DEFAULT NULL,
  `supplier_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `barcode`, `sku_id`, `category_id`, `subcategory_id`, `name`, `description`, `gst_tax`, `price`, `default_unit`, `conversion_factor`, `image_path`, `supplier_id`) VALUES
(1, '100001', 'SKU001', 1, 1, 'Basmati Rice 1kg', 'Premium quality rice.', 5, 85.00, 'kg', 1, '', 1),
(2, '100002', 'SKU002', 1, 1, 'Basmati Rice 5kg', 'Premium rice bulk pack.', 5, 390.00, 'kg', 5, '', 1),
(3, '100003', 'SKU003', 2, 3, 'Toothpaste 150g', 'Mint fresh gel.', 12, 60.00, 'pcs', 1, '', 2),
(4, '100004', 'SKU004', 2, 3, 'Toothbrush Soft', 'Soft bristles, pack of 2.', 12, 40.00, 'pcs', 1, '', 2),
(5, '100005', 'SKU005', 3, 5, 'T-shirt Cotton', 'Round neck, M-size.', 18, 299.00, 'pcs', 1, '', 3),
(6, '100006', 'SKU006', 3, 5, 'Jeans Slim Fit', 'Blue denim, 32 waist.', 18, 899.00, 'pcs', 1, '', 3),
(7, '100007', 'SKU007', 4, 6, 'LED Bulb 9W', 'Energy-saving bulb.', 18, 120.00, 'pcs', 1, '', 4),
(8, '100008', 'SKU008', 4, 6, 'Extension Cord 4 Plug', 'With surge protector.', 18, 350.00, 'pcs', 1, '', 4),
(9, '100009', 'SKU009', 5, 7, 'Notebook A4', '200 pages, ruled.', 12, 55.00, 'pcs', 1, '', 5),
(10, '100010', 'SKU010', 5, 7, 'Gel Pen Blue', 'Smooth writing, pack of 5.', 12, 75.00, 'pcs', 1, '', 5);

-- --------------------------------------------------------

--
-- Table structure for table `sales`
--

CREATE TABLE `sales` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `customer_name` varchar(100) NOT NULL,
  `quantity` float NOT NULL,
  `price` float NOT NULL,
  `gst` float NOT NULL,
  `total_price` float NOT NULL,
  `sale_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales`
--

INSERT INTO `sales` (`id`, `product_id`, `customer_name`, `quantity`, `price`, `gst`, `total_price`, `sale_date`) VALUES
(1, 1, 'Customer1', 3, 85, 5, 267.75, '2025-07-25 10:31:05'),
(2, 6, 'Customer2', 3, 899, 18, 3182.46, '2025-07-25 10:31:24'),
(3, 6, 'Customer3', 5, 899, 18, 5304.1, '2025-07-25 10:33:36'),
(4, 10, 'Customer4', 20, 75, 12, 1680, '2025-07-25 10:34:17'),
(5, 1, 'Customer5', 1, 85, 5, 89.25, '2025-07-25 10:35:08');

-- --------------------------------------------------------

--
-- Table structure for table `subcategories`
--

CREATE TABLE `subcategories` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `category_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subcategories`
--

INSERT INTO `subcategories` (`id`, `name`, `category_id`) VALUES
(1, 'Rice', 1),
(2, 'Pulses', 1),
(3, 'Dental', 2),
(4, 'Skin Care', 2),
(5, 'Men’s Wear', 3),
(6, 'Women’s Wear', 3),
(7, 'Home Electricals', 4),
(8, 'Mobile Accessories', 4),
(9, 'Office Essentials', 5),
(10, 'Art Supplies', 5);

-- --------------------------------------------------------

--
-- Table structure for table `suppliers`
--

CREATE TABLE `suppliers` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `suppliers`
--

INSERT INTO `suppliers` (`id`, `name`) VALUES
(1, 'FoodSupplier1'),
(2, 'FMCGExpress'),
(3, 'StyleMart'),
(4, 'PowerWorld'),
(5, 'NoteHub');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('admin','operator') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`, `role`) VALUES
(1, 'admin', '$2b$12$/I58eymKkHhc.TJRi4YY4.v3BwPMKGRdFjpbnz13X9CrTtaJp7nIW', 'admin'),
(2, 'operator1', '$2b$12$HeZ2yqLJHKDm94bjJQe7be1GQV5B9GZcM5/AAi7HHMAip7OAJdCce', 'operator'),
(3, 'operator2', '$2b$12$KWUn5/P2uAnANEyVU2Hrw.j/whJkft.ROC2Hr3x/da25iqjdk/CYS', 'operator');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `goods_receiving`
--
ALTER TABLE `goods_receiving`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `fk_goods_supplier` (`supplier_id`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `supplier_id` (`supplier_id`),
  ADD KEY `fk_subcategory` (`subcategory_id`);

--
-- Indexes for table `sales`
--
ALTER TABLE `sales`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `subcategories`
--
ALTER TABLE `subcategories`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `goods_receiving`
--
ALTER TABLE `goods_receiving`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `sales`
--
ALTER TABLE `sales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `subcategories`
--
ALTER TABLE `subcategories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `goods_receiving`
--
ALTER TABLE `goods_receiving`
  ADD CONSTRAINT `fk_goods_supplier` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `goods_receiving_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Constraints for table `inventory`
--
ALTER TABLE `inventory`
  ADD CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `fk_subcategory` FOREIGN KEY (`subcategory_id`) REFERENCES `subcategories` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  ADD CONSTRAINT `products_ibfk_3` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`);

--
-- Constraints for table `sales`
--
ALTER TABLE `sales`
  ADD CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Constraints for table `subcategories`
--
ALTER TABLE `subcategories`
  ADD CONSTRAINT `subcategories_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
