import { QiaomuCounterShapeUtil } from './qiaomuCounterShape.js'

export default function ({ config }) {
	config.shapeUtils.push(QiaomuCounterShapeUtil)
	return config
}
