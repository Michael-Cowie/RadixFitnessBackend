/*
  Warnings:

  - Added the required column `date` to the `WeightRecord` table without a default value. This is not possible if the table is not empty.

*/
-- RedefineTables
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_WeightRecord" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "weight" DECIMAL NOT NULL,
    "date" DATETIME NOT NULL,
    "ownerId" INTEGER NOT NULL,
    CONSTRAINT "WeightRecord_ownerId_fkey" FOREIGN KEY ("ownerId") REFERENCES "Profile" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO "new_WeightRecord" ("id", "ownerId", "weight") SELECT "id", "ownerId", "weight" FROM "WeightRecord";
DROP TABLE "WeightRecord";
ALTER TABLE "new_WeightRecord" RENAME TO "WeightRecord";
PRAGMA foreign_key_check;
PRAGMA foreign_keys=ON;
