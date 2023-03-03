import type { RequestHandler } from '@sveltejs/kit'
import * as bcrypt from 'bcrypt'

import {db } from '../../api/database'

export const post: RequestHandler = async ({request}) => {
    const form = await request.formData()
    const username = form.get('username')
    const password = form.get('password')

    console.log(form)

    return{username, password}
}