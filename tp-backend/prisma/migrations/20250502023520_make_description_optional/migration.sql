/*
  Warnings:

  - The primary key for the `_InvoiceTasks` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - A unique constraint covering the columns `[A,B]` on the table `_InvoiceTasks` will be added. If there are existing duplicate values, this will fail.

*/
-- AlterTable
ALTER TABLE "Task" ALTER COLUMN "updatedAt" DROP DEFAULT;

-- AlterTable
ALTER TABLE "_InvoiceTasks" DROP CONSTRAINT "_InvoiceTasks_AB_pkey";

-- CreateIndex
CREATE UNIQUE INDEX "_InvoiceTasks_AB_unique" ON "_InvoiceTasks"("A", "B");
