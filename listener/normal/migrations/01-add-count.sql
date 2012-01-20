ALTER TABLE `error_error` ADD COLUMN `count` integer NOT NULL DEFAULT 1;
CREATE INDEX `error_error_count` ON `error_error` (`count`);
