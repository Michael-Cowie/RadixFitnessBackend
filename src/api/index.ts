import express from 'express';

import ProfileResponse from '../interfaces/ProfileResponse';
import { prisma } from '../db';
import { checkJwt } from '../middlewares';
import { createProfile, extractUidFromRequest, getProfile, getProfileFromRequest } from '../lib/Profile';
import { getWeights, logWeight } from '../lib/Weight';

const router = express.Router();

/**
 * Fetch a user's profile
 * 
 * GET /api/v1/get-profile
 * 
 * Responds:
 * Not Found - 404
 * Found - 200 with ProfileResponse
 * 
 * Auth: required, no scopes
 */
router.get('/profile', checkJwt, async (req: any, res) => {
  let profile = await getProfileFromRequest(req);

  if (profile === null) {
    return res.status(404).send("Not Found")
  }

  res.json(profile);
});

/**
 * Create a user's profile
 * 
 * GET /api/v1/profile
 *  * 
 * Auth: required, no scopes
 */
router.post('/profile', checkJwt, async (req: any, res) => {
  // Fetch users JWT claims
  const uid = extractUidFromRequest(req);

  // Will create a profile if one doesn't exist
  const profile = await createProfile(uid, req.body.name)

  res.json(profile);
});

router.post('/weight', checkJwt, async (req, res) => {
  const profile = await getProfileFromRequest(req);

  logWeight(profile, req.body.weight)

  res.sendStatus(200)
})

router.get('/weight', checkJwt, async (req, res) => {
  const profile = await getProfileFromRequest(req);
  const weights = await getWeights(profile)

  res.json(weights)
})

export default router;
