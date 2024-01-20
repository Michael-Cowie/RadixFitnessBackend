import { prisma } from "../db"


export const getProfile = async (uid: string) => {
    return await prisma
        .profile
        .findFirst({ where: { uid: uid } })
}

export const getProfileFromRequest = async (req:any) => {
    const uid = extractUidFromRequest(req);
    return getProfile(uid)
}

export const createProfile = async (uid: string, name: string) => {
    const existingProfile = getProfile(uid);

    // Already has a profile
    if (existingProfile !== null) {
        return existingProfile
    }

    const profile = await prisma.profile.create({
        data: {
            uid: uid,
            name: name,
        }
    })

    return profile;
}

export const extractUidFromRequest = (req: any) => {
    const authPayload = req.auth.payload;
    const userId = authPayload.sub;
    
    return userId;
}