import { HTMLContainer, Rectangle2d, ShapeUtil, T, resizeBox } from 'tldraw'
import { createElement } from 'react'

export class QiaomuCounterShapeUtil extends ShapeUtil {
	static type = 'qiaomu-counter-v1'
	static props = { w: T.number, h: T.number, count: T.number }

	getDefaultProps() {
		return { w: 260, h: 140, count: 0 }
	}

	getGeometry(shape) {
		return new Rectangle2d({ width: shape.props.w, height: shape.props.h, isFilled: true })
	}

	component(shape) {
		return createElement(
			HTMLContainer,
			{
				style: {
					display: 'grid',
					placeItems: 'center',
					border: '2px solid #2563eb',
					borderRadius: 20,
					background: '#eff6ff',
					color: '#172554',
					font: '700 40px system-ui',
				},
				'aria-label': 'Clickable counter',
			},
			String(shape.props.count)
		)
	}

	getIndicatorPath(shape) {
		const path = new Path2D()
		path.roundRect(0, 0, shape.props.w, shape.props.h, 20)
		return path
	}

	onResize(shape, info) {
		return resizeBox(shape, info)
	}
}
