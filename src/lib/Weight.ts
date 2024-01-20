import { prisma } from "../db"

export const logWeight = async (profile: any, weight: number) => {
    prisma.weightRecord.create({
        data: {
            weight: weight,
            date: new Date(Date.now()),
            ownerId: profile.id,
        }
    }).catch(err => console.error(err))
}

export const getWeights = async (profile: any) => {
    const weights = await prisma.weightRecord.findMany({
        where: {
            ownerId: profile.id
        }
    })

    const dataset = weights.map(w => {
        return {
            name: w.date,
            weight: w.weight
        }
    })

    return dataset;
}